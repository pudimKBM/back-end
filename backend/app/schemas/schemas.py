from pydantic import BaseModel, Field, validator,EmailStr 
  
class CardInfoSchema(BaseModel):  
    card_number: str = Field(..., min_length=16, max_length=16)  
  
    @validator('card_number')  
    def validate_card_number(cls, v):  
        if not v.isdigit():  
            raise ValueError('Card number must be numeric')  
        return v  
class UserValidateSchema(BaseModel):  
    mail: EmailStr  
    password: str = Field(..., min_length=8)
    
    @validator('password')
    def validate_password_length(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v

    @validator('mail')
    def validate_mail(cls, v):
        if not v:
            raise ValueError('Invalid email')
        # You can add more sophisticated email validation logic here if needed
        return v