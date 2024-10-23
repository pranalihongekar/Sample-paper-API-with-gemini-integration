from motor.motor_asyncio import AsyncIOMotorClient

# MongoDB Setup
MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)
db = client.sample_paper_db
papers_collection = db.papers
tasks_collection = db.tasks

