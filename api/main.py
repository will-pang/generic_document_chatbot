from fastapi import FastAPI, File, UploadFile, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
from bson.objectid import ObjectId
from fastapi.middleware.cors import CORSMiddleware
from langchain_community.chat_models import ChatOpenAI
from pydantic import BaseModel
import uuid
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
    context_from_file: str
    session_id: str

# Initialize LangChain with your API key and model
llm = ChatOpenAI(openai_api_key=os.getenv("OPENAI_API_KEY"), model="gpt-3.5-turbo")

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    
    session_id = str(uuid.uuid4())
    content = await file.read()  # Read file content

    # Store in MongoDB
    document = {
        "session_id": session_id,
        "filename": file.filename,
        "content_type": file.content_type,
        "content": content.decode("utf-8"),  
    }
    
    result = await collection.insert_one(document)

    return {"message": "File uploaded successfully", "file_id": str(result.inserted_id), "session_id": session_id}

@app.get("/retrieve/")
async def get_latest_text():
    record = await collection.find_one(sort=[("_id", -1)])
    if record:
        return {"text": record["content"], "session_id": record["session_id"]}
    raise HTTPException(status_code=404, detail="No text found")

@app.post("/chat/")
async def chat_with_llm(request: MessageRequest):
    try:
        prompt = f'''You are an assistant explaining a medical document to a patient. 
        The medical document is: {request.context_from_file}. 
        The patient's question is: {request.message}. If you don't know the answer, say "I don't know".'''

        # Use LangChain to get a response from the LLM
        response = llm.invoke(prompt)
        return {"response": response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))