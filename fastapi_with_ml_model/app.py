from fastapi import FastAPI
import pickle
from pydantic import BaseModel, Field, computed_field
from typing import Optional, Literal, Annotated
import pandas as pd
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware


#import ML model
with open("model.pkl","rb") as f:
    model = pickle.load(f)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# pydantic model to validate data
class UserInput(BaseModel):
    age : int = Field(..., gt=0, le=120, description="Age of the user")
    weight : float = Field(..., gt=0, description="Weight of the user")
    height : float = Field(..., gt=0, lt=2.5, description="Height of the user")
    income_lpa : float = Field(..., description="Annual income of user")
    smoker : bool = Field(..., description="True or False")
    city : str = Field(..., description="City of user")
    occupation : Annotated[Literal["retired", "freelancer","student","government_job","business_owner","unemployed","private_job"], Field(..., description="Occupation of user")]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height **2),2)
        return bmi
    
    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        return "senior"
    
    @computed_field
    @property
    def city_tier(self) -> int:
        if self.city in ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]:
            return 1
        elif self.city in [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"]:
            return 2
        else :
            return 3
        
@app.get("/")
def msg():
    return {"Message" : "ML model prediction"}

@app.post("/predict")
def predict_data(data:UserInput):
    
    input_df = pd.DataFrame([{
        "bmi" : data.bmi,
        "age_group" : data.age_group,
        "lifestyle_risk" : data.lifestyle_risk,
        "city_tier" : data.city_tier,
        "income_lpa" : data.income_lpa,
        "occupation" : data.occupation  
    }])

    prediction = model.predict(input_df)[0]

    return JSONResponse(status_code=200,content={"Predicted_content": prediction})
