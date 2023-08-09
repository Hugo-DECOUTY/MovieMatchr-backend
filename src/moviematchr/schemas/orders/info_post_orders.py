from typing import Sequence

from pydantic import BaseModel, validator
from moviematchr.utils.params_validation import test_email
from moviematchr.schemas.licences.licences import TypeLicenceEnum
from moviematchr.schemas.account.user import Type2FA


class UsersDict(BaseModel):
    email: str
    type_2fa: int
    licence_type: int
    firstname: str
    lastname: str

    @validator("email")
    # pylint: disable=no-self-argument
    def email_must_be_valid(cls, v):
        if test_email(v) is False:
            raise ValueError("Invalid email")
        return v

    @validator("licence_type")
    # pylint: disable=no-self-argument
    def licence_type_must_be_valid(cls, v):
        if v not in (
            TypeLicenceEnum.DOCTOR.value,
            TypeLicenceEnum.MEDICAL_STAFF.value,
            TypeLicenceEnum.NON_MEDICAL_STAFF.value,
            TypeLicenceEnum.HDS_LOCAL_ADMIN.value,
            TypeLicenceEnum.MICROPORT_STAFF.value,
        ):
            raise ValueError("Invalid licence type")
        return v

    @validator("type_2fa")
    # pylint: disable=no-self-argument
    def type_2fa_must_be_valid(cls, v):
        if v not in (Type2FA.EMAIL.value, Type2FA.MOBILE_APP.value):
            raise ValueError("Invalid 2FA type")
        return v


class InfoPostOrders(BaseModel):
    demo_flag: bool
    company_only: bool
    sharing_authorization: bool
    order_id: str
    local_admin_email: str
    local_admin_firstname: str
    local_admin_lastname: str
    billing_type: int
    country: str
    workplace: str
    service: str
    users: Sequence[UsersDict]
    seller_email: str
    seller_firstname: str
    seller_lastname: str
    seller_phone: str

    @validator("local_admin_email")
    # pylint: disable=no-self-argument
    def local_admin_email_must_be_valid(cls, v):
        if test_email(v) is False:
            raise ValueError("Invalid email")
        return v

    @validator("local_admin_firstname")
    # pylint: disable=no-self-argument
    def local_admin_firstname_must_be_valid(cls, v):
        if len(v) == 0:
            raise ValueError("Invalid firstname")
        return v

    @validator("local_admin_lastname")
    # pylint: disable=no-self-argument
    def local_admin_lastname_must_be_valid(cls, v):
        if len(v) == 0:
            raise ValueError("Invalid lastname")
        return v

    @validator("workplace")
    # pylint: disable=no-self-argument
    def workplace_must_be_valid(cls, v):
        if len(v) == 0:
            raise ValueError("Invalid workplace")
        return v

    @validator("service")
    # pylint: disable=no-self-argument
    def service_must_be_valid(cls, v):
        if len(v) == 0:
            raise ValueError("Invalid service")
        return v

    @validator("users")
    # pylint: disable=no-self-argument
    def users_must_be_valid(cls, v):
        if len(v) > 14:
            raise ValueError("Invalid users")
        return v

    @validator("seller_email")
    # pylint: disable=no-self-argument
    def seller_email_must_be_valid(cls, v):
        if test_email(v) is False:
            raise ValueError("Invalid email")
        return v

    @validator("seller_firstname")
    # pylint: disable=no-self-argument
    def seller_firstname_must_be_valid(cls, v):
        if len(v) == 0:
            raise ValueError("Invalid firstname")
        return v

    @validator("seller_lastname")
    # pylint: disable=no-self-argument
    def seller_lastname_must_be_valid(cls, v):
        if len(v) == 0:
            raise ValueError("Invalid lastname")
        return v
