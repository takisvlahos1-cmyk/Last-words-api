from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx, os, time

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DAILY_API_KEY = os.getenv("DAILY_API_KEY", "")

@app.post("/create-room")
async def create_room():
    async with httpx.AsyncClient() as client:
        res = await client.post(
            "https://api.daily.co/v1/rooms",
            headers={"Authorization": f"Bearer {DAILY_API_KEY}", "Content-Type": "application/json"},
            json={"properties": {"exp": int(time.time())+3600, "enable_chat": False, "start_video_off": True, "max_participants": 2}}
        )
        d = res.json()
        return {"url": d.get("url"), "name": d.get("name")}

@app.get("/health")
async def health():
    return {"status": "ok"}
