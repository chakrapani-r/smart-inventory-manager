from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from dbconnection import engine
import model

model.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/', response_class=HTMLResponse)
async def home():
    return '''
    <html></body>
    <center>
    <h1>Welcome to Smart Inventory Manager! </h1>
    Go to <a href="/docs">Documentation</>
    <center>
    </body></html>
    '''
