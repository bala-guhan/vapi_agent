from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from vapi import Vapi

load_dotenv()
VAPI_PRIVATE_API_KEY = os.getenv('VAPI_PRIVATE_API_KEY')
VAPI_PHONE_NUMBER_ID = os.getenv('VAPI_PHONE_NUMBER_ID')
PRIYA_VAPI_ID = os.getenv('PRIYA_VAPI_ID')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PatientForm(BaseModel):
    name: str
    email: str
    dob: str
    patientId: str

@app.get('/hello')
def hello():
    return "Server up and running!"

@app.post('/patients')
def form_submission(form: PatientForm):
    print("Received form data:", form.dict())  # This prints to the terminal
    try: 
        res = trigger_voice_agent()
        print(f"Result from vapi : {res}")
        return {"message": res}
    except Exception as e:
        print("Error while initiating the call")
        return {"error" : e}

@app.post('/trigger-voice-agent')
def trigger_voice_agent():
    client = Vapi(token=VAPI_PRIVATE_API_KEY)
    try:
        response = client.calls.create(
            assistant_id=PRIYA_VAPI_ID,
            phone_number_id=VAPI_PHONE_NUMBER_ID, 
            customer={
                "name": "Bala Guhanesh",
                'number': "+919500664509"
            }
        )
        return {"status": "success", "response": response}
    except Exception as e:
        return {"status": "error", "detail": str(e)}