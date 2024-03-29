from pydantic import BaseModel


class BaseEntity(BaseModel):
    class ConfigDict:
        from_attributes = True
