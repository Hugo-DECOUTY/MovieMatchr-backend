from pydantic import BaseModel


class InfoPatchDemoFlag(BaseModel):
    demo_flag: bool
