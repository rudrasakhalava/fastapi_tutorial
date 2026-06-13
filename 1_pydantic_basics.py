from pydantic import BaseModel, EmailStr, AnyUrl
from typing import List, Dict, Optional

class Patient(BaseModel):
    name : str
    email : EmailStr
    linkedIn_url : AnyUrl
    age : int
    weight : float
    married : bool = False                  # set default value = "False" 
    allergies : Optional[List[str]] = None  # make feild oprtional and also set default value = "None"
    contact_detail : Dict[str,str]

def patient_data(patient : Patient):
    print(patient.name)
    print(patient.age)
    print(patient.email)
    print(patient.linkedIn_url)
    print(patient.weight)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact_detail)

patient_info = {"name" : "Rudra", "linkedIn_url" : "https://linkedin.com", "email" : "abc@gmail.com", "age" : 20, "weight" : 70.5, "married" : False, "allergies":["pollen","dust"], "contact_detail" : {"mobile":"7584263594"}}

patient1 = Patient(**patient_info)

patient_data(patient1)