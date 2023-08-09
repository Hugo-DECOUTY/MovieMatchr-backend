import asyncio
from typing import Sequence

from adminplatform.schemas.orders.orders import Orders, StateOrderEnum
from adminplatform.schemas.licences.licences import Licences

from adminplatform.services.orders import get_orders_dal, update_order_dal
from adminplatform.services.licences import (
    get_licences_from_order_dal,
    update_licence_dal,
)
from adminplatform.services.keycloak.put.put_user_licence_id_in_keycloak import (
    put_user_licence_id_in_keycloak,
)

from adminplatform.utils.utils import session_locale
from adminplatform.utils.actual_time_in_ms import actual_time_in_ms

MS_PER_YEAR = 31536000000
MS_PER_MONTH = 2628000000
S_DAY = 86400


async def desactivation_licences_daemon():
    db = session_locale()
    while True:
        orders: Sequence[Orders] = await get_orders_dal(db)

        actual_time = actual_time_in_ms()

        for order in orders:
            if order.demo_flag:
                if actual_time - order.order_accepted_date > MS_PER_MONTH:
                    licences: Sequence[Licences] = await get_licences_from_order_dal(
                        db, order.id
                    )
                    for licence in licences:
                        licence.active = False
                        await put_user_licence_id_in_keycloak(licence.id_user)
                        await update_licence_dal(db, licence)
                    order.state_flag = StateOrderEnum.EXPIRED.value
                    await update_order_dal(db, order)

            else:
                if actual_time - order.order_accepted_date > MS_PER_YEAR:
                    licences: Sequence[Licences] = await get_licences_from_order_dal(
                        db, order.id
                    )
                    for licence in licences:
                        licence.active = False
                        await put_user_licence_id_in_keycloak(licence.id_user)
                        await update_licence_dal(db, licence)
                    order.state_flag = StateOrderEnum.EXPIRED.value
                    await update_order_dal(db, order)

        await asyncio.sleep(S_DAY)
