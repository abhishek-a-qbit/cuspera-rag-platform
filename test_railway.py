from fastapi import FastAPI
import uvicorn
import os

app = FastAPI(title="Test API")

@app.get("/")
async def root():
    return {"message": "FastAPI is working!", "status": "success", "port": os.getenv("PORT", "8000")}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "FastAPI", "port": os.getenv("PORT", "8000")}

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"Starting FastAPI on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
