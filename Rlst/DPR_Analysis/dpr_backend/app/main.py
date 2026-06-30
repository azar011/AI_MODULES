from fastapi import FastAPI
from app.routes.unit_routes import router
from app.routes.department_routes import router as department_router
from app.routes.dashboard_routes import router as dashboard_router
from app.routes.checklist_routes import router as checklist_router
from app.routes.ml_routes import router as ml_router
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI(title="DPR Dashboard API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard_router)
app.include_router(router)
app.include_router(department_router)
app.include_router(checklist_router)
app.include_router(ml_router)


@app.get("/")
def home():
    return {"message": "DPR Backend Running"}