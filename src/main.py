import threading

from fastapi import FastAPI

from src.api import router
from src.core.services.telegram_notyfication import run_bot


app = FastAPI(
    title="Complaint Handling System API",
    description="API for processing customer complaints with AI analysis",
    version="1.0.0",
)


@app.on_event("startup")
def startup_event():
    threading.Thread(target=run_bot, daemon=True).start()


app.include_router(router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
