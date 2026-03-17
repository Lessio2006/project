from pydantic import BaseModel, EmailStr, Field, ConfigDict


class OrderSchema(BaseModel):
    order_id: int
    clients_id: int
    price: float = Field(gt=0)
    product: str = Field(max_length=100)
    quantity: int = Field(gt=0)


class UserSchema(BaseModel):
    email: EmailStr = Field(max_length=50)


class ClientSchema(UserSchema):
    user_firstname: str = Field(max_length=30)
    user_lastname: str = Field(max_length=30)

    #limit = ConfigDict(extra='forbid')


class UserLoginSchema(UserSchema):
    password: str = Field(max_length=20)