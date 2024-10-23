from fastapi import FastAPI
from app.routes import papers, extract, tasks

app = FastAPI()

# Include the different routes from your app
app.include_router(papers.router)
app.include_router(extract.router)
app.include_router(tasks.router)

# You can add middleware or other global configurations here if needed


# Add a default route for the homepage
@app.get("/")
async def read_root():
    return {"message": "Welcome to ZuAI Sample Paper API"}
