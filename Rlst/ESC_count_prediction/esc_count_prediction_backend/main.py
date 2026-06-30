from fastapi import FastAPI
from app.api.prediction import router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Escalation Prediction System")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)


@app.get("/")
def home():
    return {"message": "Escalation API Running"}