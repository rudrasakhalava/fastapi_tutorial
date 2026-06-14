from fastapi import FastAPI, HTTPException, Query
import json
from pydantic import BaseModel, Field, computed_field
from typing import Literal, Optional

class Student(BaseModel):
    student_id : str
    name : str = Field(..., description="Name of the student")
    age : int = Field(..., ge=5, le=30)
    marks : float = Field(..., ge=0, le=100)
    attendance : float = Field(..., ge=0, le=100)
    gender : Literal["Male","Female"] = "Male"

    @computed_field
    @property
    def grade(self) -> str :
        if self.marks >= 90:
            g = "A+"
        elif self.marks >= 80:
            g = "A"
        elif self.marks >= 70:
            g = "B"
        elif self.marks >= 60:
            g = "C"
        elif self.marks >= 40:
            g = "D"
        else :
            g = "F"
        return g

class Student_update(BaseModel):
    student_id : str
    name : Optional[str] = None
    age : Optional[int] = Field(None, ge=5, le=30)
    marks : Optional[float] = Field(None, ge=0, le=100)
    attendance : Optional[float] = Field(None, ge=0, le=100)
    gender : Literal["Male","Female"] = "Male"

def load_data():
    with open("1_student.json","r") as f:
        data = json.load(f)
    return data

def save_data(data):
    with open("1_student.json","w") as f:
        json.dump(data,f, indent=4)

app = FastAPI()

@app.get("/")
def info():
    return {"message":"Student Management API"}

@app.get("/students")
def view_data():
    d = load_data()
    return d

@app.get("/students/{sid}")
def view_data1(sid : str):
    d = load_data()
    
    for s in d:
        if s["student_id"] == sid:
            return s
    
    raise HTTPException(status_code=404, detail="student not found")
    
@app.post("/add")
def add_data(student : Student):
    d = load_data()

    for s in d:
        if s["student_id"] == student.student_id:
            raise HTTPException(status_code=409, detail="Student already exist with this id")
    
    new_student = student.model_dump()
    d.append(new_student)

    save_data(d)

    return {"message":"Data Added Successfully"}

@app.put("/edit")
def update_data(student : Student_update):
    d = load_data()

    for s in d:
        if s["student_id"] == student.student_id:
            s.update(student.model_dump(exclude_unset=True))

            if s["marks"] >= 90:
                s["grade"] = "A+"
            elif s["marks"] >= 80:
                s["grade"] = "A"
            elif s["marks"] >= 70:
                s["grade"] = "B"
            elif s["marks"] >= 60:
                s["grade"] = "C"
            elif s["marks"] >= 40:
                s["grade"] = "D"
            else :
                s["grade"] = "F"

            save_data(d)

            return {"Message" : "Data updated Successfully"}
        
    raise HTTPException(status_code=404,detail="User doesn't exists")

@app.delete("/remove/{student_id}")
def remove_data(sid : str):
    d = load_data()

    for s in d:
        if s["student_id"] == sid:
            d.remove(s)
            save_data(d)

            return {"message":"Data Deleted Successfully"}
        
    return HTTPException(status_code=404,detail="student not found")

@app.get("/search")
def search_data(name : str = Query(..., description="Enter name to search data")):
    d = load_data()

    names = [student["name"].lower() for student in d]

    if name.lower() not in names:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for s in d:
        if s["name"].lower() == name.lower():
            return s

@app.get("/sort")
def sort_data(sort_by : str = Query(..., description="you can sort by marks, attendance or age"),
              order : str = Query(..., description="You can sort in order of asc or desc")):
    
    if sort_by not in ["marks","age","attendance"]:
        raise HTTPException(status_code=400,detail="Invalid Input of sort_by")
    
    if order not in ["asc","desc"]:
        raise HTTPException(status_code=400,detail="Invalid Input of oredr")
    
    rev = False
    if order == "desc":
        rev = True
    
    d = load_data()

    sorted_data = sorted(d, key = lambda x: x.get(sort_by,0), reverse=rev)

    return sorted_data

@app.get("/top")
def top_pr():
    d = load_data()

    top_students = [s for s in d if s["marks"] > 90]

    if top_students:
        return top_students
    return {"message":"No student have 90+ marks"}

@app.get("/failed")
def failed_students():
    d = load_data()

    f_students = [s for s in d if s["grade"] == "F"]

    if f_students:
        return f_students
    return {"message":"No student have 90+ marks"}
