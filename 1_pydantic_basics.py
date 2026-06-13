from pydantic import BaseModel

class Patient(BaseModel):
    name : str
    age : int

def function1(patient : Patient):
    print(patient.name)
    print(patient.age)
    print("Data Inserted")

patient_info = {"name" : "Rudra", "age" : 30}

patient1 = Patient(**patient_info)

function1(patient1)