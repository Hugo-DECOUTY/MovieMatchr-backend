import time
import io
import pandas as pd
from fastapi import HTTPException, Request, Response
from sqlalchemy.ext.asyncio import AsyncSession

from moviematchr.schemas.orders.orders import Orders
from moviematchr.schemas.licences.licences import TypeLicenceEnum
from moviematchr.schemas.account.user import Type2FA
from moviematchr.controller.orders.get_order_about import (
    get_order_about,
)
from moviematchr.services.orders import get_order_dal

from moviematchr.services.data_storage.get_a_file_from_storage import (
    get_a_file_from_storage,
)

from moviematchr.utils.user_group import UserGroup, get_payload_and_groups


async def get_order_attachement(db: AsyncSession, request: Request, order_id: str):
    _, group = get_payload_and_groups(request.headers.get("X-USERINFO"))

    if group == UserGroup.HDS_ADMIN_MICROPORT.value:

        order: Orders = await get_order_dal(db, order_id)

        if order is None:
            raise HTTPException(status_code=404)

        file = get_a_file_from_storage(f"{order.id}/{order.order_id}.xlsx")

        if file:
            return file

        else:

            orderInformation = await get_order_about(db, request, order_id)

            df_general = pd.DataFrame()
            df_local_admin = pd.DataFrame()
            df_seller = pd.DataFrame()
            df_users = pd.DataFrame()

            headers_general = [
                "ID Order",
                "Workplace",
                "Service",
                "State",
                "Sending Date",
                "Demo",
            ]

            headers_local_admin = [
                "Local Administrateur Firstname",
                "Local Administrateur Lastname",
                "Local Administrateur Email",
            ]

            headers_seller = [
                "Seller Firstname",
                "Seller Lastname",
                "Seller Email",
            ]

            if orderInformation["seller"]["phone"]:
                headers_seller.append("Seller Phone")

            headers_users = [
                "User n°",
                "User Firstname",
                "User Lastname",
                "User Email",
                "Type 2FA" "Licence Type",
            ]

            row_general = dict()
            row_general.update(
                {
                    "ID Order": order.order_id,
                    "Workplace": order.workplace,
                    "Service": order.service,
                    "State": "ACCEPTED" if order.state_flag == 0 else "EXPIRED",
                    "Sending Date": time.strftime(
                        "%H:%M:%S %d/%m/%Y", time.localtime(order.sending_date / 1000.0)
                    ),
                    "Demo": "NO" if order.demo_flag == 0 else "YES",
                }
            ),

            row_local_admin = dict()
            row_local_admin.update(
                {
                    "Local Administrateur Firstname": orderInformation["local_admin"][
                        "firstname"
                    ],
                    "Local Administrateur Lastname": orderInformation["local_admin"][
                        "lastname"
                    ],
                    "Local Administrateur Email": orderInformation["local_admin"][
                        "email"
                    ],
                }
            ),

            row_seller = dict()
            row_seller.update(
                {
                    "Seller Firstname": orderInformation["seller"]["firstname"],
                    "Seller Lastname": orderInformation["seller"]["lastname"],
                    "Seller Email": orderInformation["seller"]["email"],
                }
            ),

            if orderInformation["seller"]["phone"]:
                row_seller.update({"Seller Phone": orderInformation["seller"]["phone"]})

            users_row_list = []

            for i in range(len(orderInformation["users"])):
                current_row = dict()
                current_row.update({"User n°": str(i + 1)})
                current_row.update(
                    {"User Firstname": orderInformation["users"][i]["firstname"]}
                )
                current_row.update(
                    {"User Lastname": orderInformation["users"][i]["lastname"]}
                )
                current_row.update(
                    {"User Email": orderInformation["users"][i]["email"]}
                )
                if orderInformation["users"][i]["type_2fa"] == Type2FA.EMAIL.value:
                    current_row.update({"2FA Type": "EMAIL"})
                if orderInformation["users"][i]["type_2fa"] == Type2FA.MOBILE_APP.value:
                    current_row.update({"2FA Type": "MOBILE_APP"})
                if (
                    orderInformation["users"][i]["licence_type"]
                    == TypeLicenceEnum.DOCTOR.value
                ):
                    current_row.update({"Licence Type": "DOCTOR"})

                elif (
                    orderInformation["users"][i]["licence_type"]
                    == TypeLicenceEnum.MEDICAL_STAFF.value
                ):
                    current_row.update({"Licence Type": "MEDICAL_STAFF"})

                elif (
                    orderInformation["users"][i]["licence_type"]
                    == TypeLicenceEnum.NON_MEDICAL_STAFF.value
                ):
                    current_row.update({"Licence Type": "NON_MEDICAL_STAFF"})

                else:
                    current_row.update({"Licence Type": ""})

                users_row_list.append(current_row)

            df_general = df_general.append(row_general, ignore_index=True)
            df_local_admin = df_local_admin.append(row_local_admin, ignore_index=True)
            df_seller = df_seller.append(row_seller, ignore_index=True)
            df_users = df_users.append(users_row_list, ignore_index=True)

            # Create a BytesIO object to store the Excel file in memory
            output = io.BytesIO()

            # Define the Excel writer
            writer = pd.ExcelWriter(output, engine="xlsxwriter")

            df_general.to_excel(
                writer, sheet_name="Sheet1", index=False, header=headers_general
            )
            df_local_admin.to_excel(
                writer,
                sheet_name="Sheet1",
                index=False,
                header=headers_local_admin,
                startrow=3,
            )
            df_seller.to_excel(
                writer,
                sheet_name="Sheet1",
                index=False,
                header=headers_seller,
                startrow=6,
            )

            if len(orderInformation["users"]) > 0:
                df_users.to_excel(
                    writer,
                    sheet_name="Sheet1",
                    index=False,
                    header=headers_users,
                    startrow=9,
                )

            # Get the xlsxwriter workbook and worksheet objects
            workbook = writer.book
            worksheet = writer.sheets["Sheet1"]

            worksheet.conditional_format(
                "A1:Z1",
                {"type": "no_blanks", "format": workbook.add_format({"border": 1})},
            )
            worksheet.conditional_format(
                "A1:Z1",
                {
                    "type": "no_blanks",
                    "format": workbook.add_format({"bg_color": "#D3D3D3"}),
                },
            )
            worksheet.conditional_format(
                "A1:Z1",
                {
                    "type": "no_blanks",
                    "format": workbook.add_format({"align": "center"}),
                },
            )
            worksheet.conditional_format(
                "A2:Z2",
                {"type": "no_blanks", "format": workbook.add_format({"border": 1})},
            )
            worksheet.conditional_format(
                "A2:Z2",
                {"type": "no_blanks", "format": workbook.add_format({"align": "left"})},
            )

            worksheet.conditional_format(
                "A4:Z4",
                {"type": "no_blanks", "format": workbook.add_format({"border": 1})},
            )
            worksheet.conditional_format(
                "A4:Z4",
                {
                    "type": "no_blanks",
                    "format": workbook.add_format({"bg_color": "#D3D3D3"}),
                },
            )
            worksheet.conditional_format(
                "A4:Z4",
                {
                    "type": "no_blanks",
                    "format": workbook.add_format({"align": "center"}),
                },
            )
            worksheet.conditional_format(
                "A5:Z5",
                {"type": "no_blanks", "format": workbook.add_format({"border": 1})},
            )
            worksheet.conditional_format(
                "A5:Z5",
                {"type": "no_blanks", "format": workbook.add_format({"align": "left"})},
            )

            worksheet.conditional_format(
                "A7:Z7",
                {"type": "no_blanks", "format": workbook.add_format({"border": 1})},
            )
            worksheet.conditional_format(
                "A7:Z7",
                {
                    "type": "no_blanks",
                    "format": workbook.add_format({"bg_color": "#D3D3D3"}),
                },
            )
            worksheet.conditional_format(
                "A7:Z7",
                {
                    "type": "no_blanks",
                    "format": workbook.add_format({"align": "center"}),
                },
            )
            worksheet.conditional_format(
                "A8:Z8",
                {"type": "no_blanks", "format": workbook.add_format({"border": 1})},
            )
            worksheet.conditional_format(
                "A8:Z8",
                {"type": "no_blanks", "format": workbook.add_format({"align": "left"})},
            )

            worksheet.conditional_format(
                "A10:Z10",
                {"type": "no_blanks", "format": workbook.add_format({"border": 1})},
            )
            worksheet.conditional_format(
                "A10:Z10",
                {
                    "type": "no_blanks",
                    "format": workbook.add_format({"bg_color": "#D3D3D3"}),
                },
            )
            worksheet.conditional_format(
                "A10:Z10",
                {
                    "type": "no_blanks",
                    "format": workbook.add_format({"align": "center"}),
                },
            )
            for i in range(11, len(orderInformation["users"]) + 11):
                worksheet.conditional_format(
                    f"A{i}:Z{i}",
                    {"type": "no_blanks", "format": workbook.add_format({"border": 1})},
                )
                worksheet.conditional_format(
                    f"A{i}:Z{i}",
                    {
                        "type": "no_blanks",
                        "format": workbook.add_format({"align": "left"}),
                    },
                )

            for i in range(len(headers_general)):
                worksheet.set_column(
                    i,
                    i,
                    len(headers_general[i]) if len(headers_general[i]) > 30 else 30,
                )

            # Close the Excel writer
            writer.save()

            # Reset the file pointer to the beginning of the stream
            output.seek(0)

            # Return the BytesIO object as a response with the appropriate content type and headers
            return Response(
                content=output.getvalue(),
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-Disposition": 'attachment; filename="order.xlsx"'},
            )

    raise HTTPException(status_code=403)
