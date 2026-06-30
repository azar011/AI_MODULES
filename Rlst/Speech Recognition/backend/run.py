import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


# celery -A app.tasks worker --pool=threads --concurrency=2 --loglevel=info
# uvicorn app.main:app --reload                                            
