from fastapi import FastAPI, Request
import json

app = FastAPI()

@app.post("/webhook")
async def webhook_handler(request: Request):
    data = await request.json()
    # Сохраняем данные в файл
    with open("received_data.json", "w") as file:
        json.dump(data, file, indent=4)
    
    return {"message": "Data received and saved successfully"}


def start(addr = "0.0.0.0", port = 8080):
    import uvicorn
    uvicorn.run(app, host=addr, port=port)
