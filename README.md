# Sample-Paper-API-with-Gemini-Integration

1. Set Up Your Environment
2.  Install Dependencies:
3.  python -m venv venv  # Create a virtual environment
source venv/bin/activate  # Activate the virtual environment

pip install -r req.txt  # Install dependencies from your requirements file

 MongoDB:
 Make sure MongoDB is running on your local machine at mongodb://localhost:27017. You can start it with:
 sudo service mongod start

#Redis:
Ensure Redis is running on your machine at localhost:6379. You can start Redis with:
sudo service redis-server start
Environment Variables:

#Ensure your .env file is correctly configured with the following:
API_KEY=<your_google_api_key>
MONGO_URI=mongodb://localhost:27017

#You can load the environment variables with:
source .env

#Run the FastAPI Application:

#You can run the FastAPI app using uvicorn. In the root folder of your project (where main.py is located), run:
uvicorn app.main:app --reload

#Testing Your Endpoints:
Manual Testing with Curl or Postman:

#Retrieve a Sample Paper (GET /papers/{paper_id})
Upload PDF for Extraction (POST /extract/pdf): You can test this using Postman to upload a file, or you can use a curl command with --form:
Task Status (GET /tasks/{task_id})

