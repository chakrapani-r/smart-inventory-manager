from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import router
from dbconnection import engine
import model
from loguru import logger
# from logging_config import logger
from datetime import datetime

app = FastAPI(title='SmartInventoryManager', swagger_ui_parameters={"defaultModelsExpandDepth": -1})

model.Base.metadata.create_all(bind=engine)

# Configure loguru logger
logger.add("logs/application.log", rotation="500 MB", retention="10 days", level="DEBUG")
logger.add("logs/access.log", rotation="1 day", retention="7 days", level="INFO", format="{time:YYYY-MM-DD HH:mm:ss} - {message}")

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()
    response = await call_next(request)
    end_time = datetime.now()

    processing_time = (end_time - start_time).total_seconds() * 1000  # Convert to milliseconds

    logger.info(
        "{ip} - HTTP {method} {url} - Status: {status_code} - Duration: {duration:.2f}ms",
        method=request.method,
        url=request.url,
        status_code=response.status_code,
        duration=processing_time,
        ip=request.client.host
    )

    return response


@app.get('/', response_class=HTMLResponse, include_in_schema=False)
async def home():
    return '''
    <html></body>
    <center>
    <h1>Welcome to Smart Inventory Manager! </h1>
    Go to <a href="/docs">Documentation</>
    <center>
    </body></html>
    '''

app.include_router(router.router)
