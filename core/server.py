from fastapi import FastAPI, Request
from lib.helper import TriggerDataModel
from lib.logger import logging as log

from telegram import api as tgapi

app = FastAPI()

@app.post("/webhook")
async def webhook_handler(request: Request):
    valid_data = None
    try:
        data = await request.json()
        valid_data = TriggerDataModel(**data)
    except Exception as err:
        log.error(err)
        return
    
    try:
        await tgapi.simple_send_message(tgapi.chid, str(valid_data))
        return {"message": "Data received"}
    except Exception as err:
        log.error(err)
        return


def start(addr = "0.0.0.0", port = 8080):
    import uvicorn
    uvicorn.run(app, host=addr, port=port)

async def start_async():
    from uvicorn import Server, Config
    config = Config(app, host="0.0.0.0", port=8080)
    server = Server(config)
    await server.serve()

