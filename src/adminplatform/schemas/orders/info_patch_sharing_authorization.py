from pydantic import BaseModel


class InfoPatchSharingAuthorization(BaseModel):
    sharing_authorization: bool
