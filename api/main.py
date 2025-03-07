from fastapi import FastAPI, File, UploadFile, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.chat_models import ChatOpenAI
from pydantic import BaseModel
# Load environment variables
load_dotenv(override=True)

# FastAPI instance
app = FastAPI()

# Allow requests from your frontend
origins = [
    "http://10.0.0.34:3000",  # Your frontend URL
    "http://localhost:3000",  # Local frontend (if needed)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow only specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


# MongoDB connection
client = AsyncIOMotorClient(os.getenv("MONGO_URI"))
db = client[f"{os.getenv("DB")}"]
collection = db[f"{os.getenv("COLLECTION")}"]

# Define a request model
class MessageRequest(BaseModel):
    message: str

# Initialize LangChain with your API key and model
llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-3.5-turbo")

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()  # Read file content

    # Store in MongoDB
    document = {
        "filename": file.filename,
        "content_type": file.content_type,
        "content": content.decode("utf-8"),  
    }
    
    result = await collection.insert_one(document)

    return {"message": "File uploaded successfully", "file_id": str(result.inserted_id)}

@app.get("/retrieve/")
async def get_latest_text():
    text = await collection.find_one(sort=[("_id", -1)])
    if text:
        return {"text": text["content"]}
    raise HTTPException(status_code=404, detail="No text found")

@app.post("/chat/")
async def chat_with_llm(request: MessageRequest):
    try:
        # Use LangChain to get a response from the LLM
        response = llm.invoke(request.message)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))