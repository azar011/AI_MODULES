from pydantic import BaseModel


class EscalationRequest(BaseModel):

    department: str
    checklist_name: str
    question: str
    remarks: str