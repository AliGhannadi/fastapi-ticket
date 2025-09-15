from fastapi import FastAPI, Depends, HTTPException, status, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session 
from typing import Annotated
from models import Tickets
from db import engine, SessionLocal, Base
from schemas import TicketRequest
app = FastAPI()
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close(
        )
        
db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/tickets", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Tickets).all()

@app.get("/tickets/by_id/{ticket_id}", status_code=status.HTTP_200_OK)
async def get_tickets_by_id(db: db_dependency, ticket_id: int = Path(gt=0)): 
    ticket_model = db.query(Tickets).filter(Tickets.id == ticket_id).first()
    if ticket_model is not None:
        return ticket_model
    raise HTTPException(status_code=404, detail='Item not found.')

@app.get("/tickets/by_priority/{priority}")
async def get_tickets_by_priority(db: db_dependency, priority: int = Path(gt=0)):
    ticket_model = db.query(Tickets).filter(Tickets.priority == priority).all()
    if ticket_model is not None:
        return ticket_model
    raise HTTPException(status_code=404, detail='No tickets found with this priority.')

@app.post("/tickets/create_ticket", status_code=status.HTTP_201_CREATED)
async def create_ticket(ticket_request: TicketRequest, db: db_dependency):
    ticket_model = Tickets(**ticket_request.dict())
    db.add(ticket_model)
    db.commit()
@app.put("/tickets/update_ticket/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_ticket(db: db_dependency, ticket_request: TicketRequest, ticket_id: int = Path(gt=0)):
    ticket_model = db.query(Tickets).filter(Tickets.id == ticket_id).first()
    if ticket_model is None:
        raise HTTPException(status_code=404, detail='Item not found.')
    ticket_model.title = ticket_request.title
    ticket_model.description = ticket_request.description
    ticket_model.priority = ticket_request.priority
    db.add(ticket_model)
    db.commit()

@app.delete("/tickets/delete_ticket/{ticket_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_ticket(db: db_dependency, ticket_id: int = Path(gt=0)):
    ticket_model = db.query(Tickets).filter(Tickets.id == ticket_id).first()
    if ticket_model is None:
        raise HTTPException(status_code=404, detail='Id not found.')
    db.delete(ticket_model)
    db.commit()
    return None