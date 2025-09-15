from pydantic import BaseModel, Field



class TicketRequest(BaseModel):
    title: str = Field(min_length=3, max_length=350)
    description: str = Field(min_length=3, max_length=350)
    priority: int = Field(lt=6, gt=0)