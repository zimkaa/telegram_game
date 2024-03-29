from pydantic import BaseModel


class BaseValueObject(BaseModel):
    class ConfigDict:
        from_attributes = True
