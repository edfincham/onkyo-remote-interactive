import time
import asyncio
import uuid
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from dataclasses import dataclass
from concurrent.futures import ProcessPoolExecutor

from onkyo import OnkyoRI


conn = OnkyoRI(pin=8)


@dataclass
class Message:
    code: int
    

def process(msg: Message):
    print(f"Processing: {msg.code}")
    conn.send(msg.code)
    return "ok"


async def process_requests(q: asyncio.Queue, pool: ProcessPoolExecutor):
    while True:
        msg = await q.get()
        loop = asyncio.get_running_loop()
        r = await loop.run_in_executor(pool, process, msg)
        q.task_done()


@asynccontextmanager
async def lifespan(app: FastAPI):
    q = asyncio.Queue()
    pool = ProcessPoolExecutor()
    asyncio.create_task(process_requests(q, pool))
    yield {"q": q, "pool": pool}
    pool.shutdown()


app = FastAPI(lifespan=lifespan)


@app.get("/enqueue")
async def add_task(request: Request, code: int):
    msg = Message(code)
    request.state.q.put_nowait(msg)
    return {"status": "okay"}
    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080)
