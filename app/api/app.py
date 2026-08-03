from fastapi import FastAPI
from pydantic import BaseModel

from app.services.recommendation_service import RecommendationService

app = FastAPI(
    title="SAP MDG Intelligent Support Assistant",
    version="1.0"
)

service = RecommendationService()


class TicketRequest(BaseModel):
    ticket: str


@app.get("/")
def home():

    return {
        "status": "Running",
        "application": "SAP MDG Intelligent Support Assistant"
    }


@app.post("/analyze-ticket")
def analyze_ticket(request: TicketRequest):

    return service.analyze_ticket(

        request.ticket

    )