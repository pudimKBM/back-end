from pydantic import BaseModel, Field, validator  
  
class CardInfoSchema(BaseModel):  
    card_number: str = Field(..., min_length=16, max_length=16)  
  
    @validator('card_number')  
    def validate_card_number(cls, v):  
        if not v.isdigit():  
            raise ValueError('Card number must be numeric')  
        return v  