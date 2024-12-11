from fastapi import FastAPI, Request
from lib.helper import TriggerDataModel
from lib.logger import logging as log
from telegram import api as tgapi
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = FastAPI()

@app.post("/webhook")
async def webhook_handler(request: Request):
    valid_data = None
    btns=None
    service_url = getenv("SERVICE_URL")
    
    try:
        data = await request.json()
        log.debug(data)
        valid_data = TriggerDataModel(**data)
        log.debug(valid_data)
    except Exception as err:
        log.error(err)
        return
    
    if service_url:
        btns = {
            "inline_keyboard" : [
                [
                    {"text": "Подробнее 🖥", "url": f"{service_url}/front/ticket.form.php?id={valid_data.ticket.id}"}
                ]
            ]
        }

    try:
        await tgapi.send_message_with_btns(tgapi.chid, str(valid_data), btns=btns)
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

