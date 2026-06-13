from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator
from typing import List, Dict, Optional

class Patient(BaseModel):
    name : str = Field(
        title="Patient's Name",
        description="Enter Patient's Full Name",
        examples=["Rudra"],
        strict=True
    )
    email : EmailStr
    linkedIn_url : AnyUrl
    age : int = Field(gt=0)
    weight : float = Field(gt=0)
    married : bool = False                  # set default value = "False" 
    allergies : Optional[List[str]] = None  # make feild oprtional and also set default value = "None"
    contact_detail : Dict[str,str]

    @field_validator("email")
    @classmethod
    def email_validator(cls, value):
        valid_domain = ["hdfc.com", "icici.com"]

        domain = value.split("@")[-1]

        if domain not in valid_domain:
            raise ValueError("Not a valid domain")
        return value
    
    @field_validator("name")
    @classmethod
    def name_validator(cls, value):
        return value.lower()
    
    @model_validator(mode = "after")
    def validate_emergency_contect(cls, model):
        if model.age > 60 and "mobile" not in model.contact_detail :
            raise ValueError("Patients older than 60 must have an emergency contact number")
        return model

def patient_data(patient : Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.linkedIn_url)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_detail)

patient_info = {"name" : "Rudra", "linkedIn_url" : "https://linkedin.com", "email" : "abc@icici.com", "age" : 20, "weight" : 70.5, "married" : False, "allergies":["pollen","dust"], "contact_detail" : {"mobile":"7584263594"}}

patient1 = Patient(**patient_info)

patient_data(patient1)