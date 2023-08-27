from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import router
from dbconnection import engine
import model
import cron

model.Base.metadata.create_all(bind=engine)

app = FastAPI(swagger_ui_parameters={"defaultModelsExpandDepth": -1})


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

app.include_router(router.router, tags=["Inventory"])
