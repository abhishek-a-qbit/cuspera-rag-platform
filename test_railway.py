from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Test API")

@app.get("/")
async def root():
    return {"message": "FastAPI is working!", "status": "success"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "FastAPI"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
