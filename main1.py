from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

from pydantic import BaseModel
from typing import Optional

class PatientBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    blood_group: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    height_cm: Optional[int] = None
    weight_kg: Optional[int] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    disease: Optional[str] = None
    doctor: Optional[str] = None
    admission_date: Optional[str] = None
    is_admitted: Optional[bool] = None
    emergency_contact: Optional[str] = None
    insurance: Optional[bool] = None

class Patient(PatientBase):
    patient_id: str

class PatientUpdate(PatientBase):
    pass

def load_data():
    with open("patients.json", "r") as f:
        return json.load(f)

def add_data(patient: Patient):
    with open("patients.json", "r") as f:
        data = json.load(f)

    # Check if patient already exists
    for p in data:
        if p["patient_id"] == patient.patient_id:
            return False

    new_patient = patient.model_dump()

    data.append(new_patient)

    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)

    return True

def update_data(patient_id: str, patient: PatientUpdate):

    with open("patients.json","r") as f:
        data = json.load(f)

    for p in data:
        if p["patient_id"] == patient_id:

            updates = patient.model_dump(exclude_unset=True,exclude_none=True)

            for key, value in updates.items():
                p[key] = value

            with open("patients.json","w") as f:
                json.dump(data,f,indent=4)

            return True

    return False

def delete_value(pid):
    with open("patients.json", "r") as f:
        data = json.load(f)

    deleted = False

    for p in data:
        if p["patient_id"] == pid:
            data.remove(p)
            deleted = True
            break

    if deleted:
        with open("patients.json", "w") as f:
            json.dump(data, f, indent=4)

    return deleted


@app.get("/")
def home():
    return {"message": "Patients Management System API"}


@app.get("/about")
def about():
    return {
        "message": "A Fully Functional API to Manage Your Patient's Records"
    }


@app.get("/view")
def read_all_data():
    return load_data()


@app.put("/update")
def update_value(patient_id: str, patient: PatientUpdate):

    updated = update_data(
        patient_id=patient_id,
        patient=patient
    )

    if updated:
        return {"message": "Patient updated successfully"}

    raise HTTPException(status_code=404,detail="User not found!!!")

@app.post("/add")
def add_value(patient : Patient):
    add = add_data(patient)
    
    if add:
        return {"message": "Patient added successfully"}

    raise HTTPException(status_code=404,detail="User not found!!!")

@app.delete("/delete")
def delete_data(p_id : str):
    deleted = delete_value(p_id)

    if deleted :
        return {"Message" : "Data Deleted Successfully"}
    raise HTTPException(status_code=404,detail="User not found!!!")

@app.get("/view/{pid}")
def show_data(pid : str = Path(..., description="ID of the patient in the DB", example="P001")):
    data = load_data()

    for p in data:
        if p["patient_id"] == pid:
            return p
        
    raise HTTPException(status_code=404,detail="User not found!!!")

@app.get("/sort")
def sorted_patients(sort_by : str = Query(description="you can sort on the basis of height, weight or age"), order : str = Query("asc", description="Sort in asc or desc order")):

    if sort_by not in ["height_cm","weight_kg","age"]:
        raise HTTPException(status_code=400, detail="Invalid field selected")
    
    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400,detail="Given Order is Invalid")

    data = load_data()

    rev = False
    if order == "desc":
        rev = True

    sorted_data = sorted(data, key= lambda x: x.get(sort_by,0), reverse=rev)

    return sorted_data