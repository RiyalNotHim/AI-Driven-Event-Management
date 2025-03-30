from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import google.generativeai as genai  
import uvicorn  
import threading  

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

genai.configure(api_key="AIzaSyDbS-NVjFAVroQTvOfKoMs8CtUvB1QKN2I") 

def chat_with_ai(user_input):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        response = model.generate_content(user_input)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

@app.get("/chat")
async def chat(request: Request):
    user_input = request.query_params.get("message", "")
    if not user_input:
        return {"response": "Please provide a message."}
    
    response = chat_with_ai(user_input)
    return {"response": response}

# Auto-start the FastAPI server in a separate thread
def run_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)

if __name__ == "__main__":
    threading.Thread(target=run_server).start()