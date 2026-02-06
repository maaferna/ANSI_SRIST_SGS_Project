from fastapi import FastAPI

app = FastAPI(title="CSIRT Microservice")

@app.get("/health")
def health():
    return {"ok": True, "service": "fastapi"}

