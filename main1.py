from fastapi import FastAPI, Path, HTTPException
import json

app = FastAPI()


def load_data():
    with open("patients.json", "r") as f:
        return json.load(f)

def add_data(
    patient_id,
    first_name=None,
    last_name=None,
    gender=None,
    age=None,
    blood_group=None,
    city=None,
    state=None,
    country=None,
    height_cm=None,
    weight_kg=None,
    phone=None,
    email=None,
    disease=None,
    doctor=None,
    admission_date=None,
    is_admitted=None,
    emergency_contact=None,
    insurance=None,
):
    with open("patients.json", "r") as f:
        data = json.load(f)

    # Check if patient already exists
    for p in data:
        if p["patient_id"] == patient_id:
            return False

    new_patient = {
        "patient_id": patient_id,
        "first_name": first_name,
        "last_name": last_name,
        "gender": gender,
        "age": age,
        "blood_group": blood_group,
        "city": city,
        "state": state,
        "country": country,
        "height_cm": height_cm,
        "weight_kg": weight_kg,
        "phone": phone,
        "email": email,
        "disease": disease,
        "doctor": doctor,
        "admission_date": admission_date,
        "is_admitted": is_admitted,
        "emergency_contact": emergency_contact,
        "insurance": insurance,
    }

    data.append(new_patient)

    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)

    return True

def update_data(
    patient_id,
    first_name=None,
    last_name=None,
    gender=None,
    age=None,
    blood_group=None,
    city=None,
    state=None,
    country=None,
    height_cm=None,
    weight_kg=None,
    phone=None,
    email=None,
    disease=None,
    doctor=None,
    admission_date=None,
    is_admitted=None,
    emergency_contact=None,
    insurance=None,
):

    with open("patients.json", "r") as f:
        data = json.load(f)

    updated = False

    for p in data:
        if p["patient_id"] == patient_id:

            if first_name is not None:
                p["first_name"] = first_name

            if last_name is not None:
                p["last_name"] = last_name

            if gender is not None:
                p["gender"] = gender

            if age is not None:
                p["age"] = age

            if blood_group is not None:
                p["blood_group"] = blood_group

            if city is not None:
                p["city"] = city

            if state is not None:
                p["state"] = state

            if country is not None:
                p["country"] = country

            if height_cm is not None:
                p["height_cm"] = height_cm

            if weight_kg is not None:
                p["weight_kg"] = weight_kg

            if phone is not None:
                p["phone"] = phone

            if email is not None:
                p["email"] = email

            if disease is not None:
                p["disease"] = disease

            if doctor is not None:
                p["doctor"] = doctor

            if admission_date is not None:
                p["admission_date"] = admission_date

            if is_admitted is not None:
                p["is_admitted"] = is_admitted

            if emergency_contact is not None:
                p["emergency_contact"] = emergency_contact

            if insurance is not None:
                p["insurance"] = insurance

            updated = True
            break

    if updated:
        with open("patients.json", "w") as f:
            json.dump(data, f, indent=4)

    return updated

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
def update_value(
    patient_id: str,
    first_name: str = None,
    last_name: str = None,
    gender: str = None,
    age: int = None,
    blood_group: str = None,
    city: str = None,
    state: str = None,
    country: str = None,
    height_cm: int = None,
    weight_kg: int = None,
    phone: str = None,
    email: str = None,
    disease: str = None,
    doctor: str = None,
    admission_date: str = None,
    is_admitted: bool = None,
    emergency_contact: str = None,
    insurance: bool = None,
):

    updated = update_data(
        patient_id=patient_id,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        age=age,
        blood_group=blood_group,
        city=city,
        state=state,
        country=country,
        height_cm=height_cm,
        weight_kg=weight_kg,
        phone=phone,
        email=email,
        disease=disease,
        doctor=doctor,
        admission_date=admission_date,
        is_admitted=is_admitted,
        emergency_contact=emergency_contact,
        insurance=insurance,
    )

    if updated:
        return {"message": "Patient updated successfully"}

    raise HTTPException(status_code=404,detail="User not found!!!")

@app.post("/add")
def add_value(
    patient_id: str,
    first_name: str = None,
    last_name: str = None,
    gender: str = None,
    age: int = None,
    blood_group: str = None,
    city: str = None,
    state: str = None,
    country: str = None,
    height_cm: int = None,
    weight_kg: int = None,
    phone: str = None,
    email: str = None,
    disease: str = None,
    doctor: str = None,
    admission_date: str = None,
    is_admitted: bool = None,
    emergency_contact: str = None,
    insurance: bool = None,
):
    add = add_data(
        patient_id=patient_id,
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        age=age,
        blood_group=blood_group,
        city=city,
        state=state,
        country=country,
        height_cm=height_cm,
        weight_kg=weight_kg,
        phone=phone,
        email=email,
        disease=disease,
        doctor=doctor,
        admission_date=admission_date,
        is_admitted=is_admitted,
        emergency_contact=emergency_contact,
        insurance=insurance,
    )
    
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
