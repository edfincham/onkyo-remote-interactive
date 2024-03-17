from fastapi import BackgroundTasks, FastAPI
from pydantic import BaseModel, validator

from onkyo import OnkyoRI


conn = OnkyoRI(pin=8)
app = FastAPI()


def is_valid_hexadecimal(number):
    try:
        int(number, base=16)
        return True
    except ValueError():
        return False


def in_12bit_range(number):
    return 0 <= number <= 4095


class Message(BaseModel):
    action: str

    @validator("action")
    def check_action(cls, v):
        if not (is_valid_hexadecimal(v) and in_12bit_range(int(v, base=16))):
            raise ValueError("Requested action not valid.")
        return v


async def process_message(msg: Message):
    conn.send(int(msg.action, base=16))
    return {"message": "Success"}


@app.post("/message")
async def add_message(message: Message, background_tasks: BackgroundTasks):
    background_tasks.add_task(process_message, message)
    return {"message": "Message sent"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
