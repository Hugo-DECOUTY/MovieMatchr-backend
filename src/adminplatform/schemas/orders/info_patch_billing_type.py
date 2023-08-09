from pydantic import BaseModel, validator
from adminplatform.schemas.orders.orders import BillingTypeEnum


class InfoPatchBillingType(BaseModel):
    billing_type: int

    @validator("billing_type")
    # pylint: disable=no-self-argument
    def check_billing_type(cls, v):
        if v not in (
            BillingTypeEnum.SIZE_1_TO_190.value,
            BillingTypeEnum.SIZE_191_TO_385.value,
            BillingTypeEnum.SIZE_386_TO_580.value,
            BillingTypeEnum.SIZE_581_TO_770.value,
            BillingTypeEnum.SIZE_771_TO_1150.value,
            BillingTypeEnum.SIZE_1151_TO_1730.value,
        ):
            raise ValueError("Billing type not valid")
        return v
