from fastapi import FastAPI, APIRouter, HTTPException
from pymongo import MongoClient
from typing import Optional, List
from pydantic import BaseModel
from bson import ObjectId
import uvicorn

client = MongoClient("mongodb://root:password@localhost:27018/")
db = client["my_db"]
cars_collection = db["cars"]

class CarCreate(BaseModel):
    marca: str
    modelo: str
    ano: int

class CarUpdate(BaseModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    ano: Optional[int] = None

class CarResponse(BaseModel):
    id: str
    marca: str
    modelo: str
    ano: int

def serialize_car(car) -> CarResponse:
    return CarResponse(
        id=str(car["_id"]),
        marca=car["marca"],
        modelo=car["modelo"],
        ano=car["ano"]
    )

def parse_object_id(car_id: str) -> ObjectId:
    try:
        return ObjectId(car_id)
    except Exception:
        raise HTTPException(status_code=400, detail="ID inválido")

def create_car(data: CarCreate) -> CarResponse:
    result = cars_collection.insert_one(data.model_dump())
    new_car = cars_collection.find_one({"_id": result.inserted_id})
    return serialize_car(new_car)

def get_all_cars() -> List[CarResponse]:
    return [serialize_car(car) for car in cars_collection.find()]

def get_car_by_id(car_id: str) -> CarResponse:
    obj_id = parse_object_id(car_id)
    car = cars_collection.find_one({"_id": obj_id})
    if not car:
        raise HTTPException(status_code=404, detail="Carro não encontrado")
    return serialize_car(car)

def update_car(car_id: str, data: CarUpdate) -> CarResponse:
    obj_id = parse_object_id(car_id)
    update_data = data.model_dump(exclude_unset=True)
    
    if not update_data:
        raise HTTPException(status_code=400, detail="Nenhum campo para atualizar")

    result = cars_collection.update_one(
        {"_id": obj_id},
        {"$set": update_data}
    )
    
    updated_car = cars_collection.find_one({"_id": obj_id})
    if not updated_car:
        raise HTTPException(status_code=404, detail="Carro não encontrado")
        
    return serialize_car(updated_car)

def delete_car(car_id: str) -> dict:
    obj_id = parse_object_id(car_id)
    result = cars_collection.delete_one({"_id": obj_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Carro não encontrado")
    return {"message": "Carro deletado com sucesso"}

router = APIRouter(prefix="/cars", tags=["Cars"])

@router.post("/", response_model=CarResponse)
def create(data: CarCreate):
    return create_car(data)

@router.get("/", response_model=List[CarResponse])
def get_all():
    return get_all_cars()

@router.get("/{car_id}", response_model=CarResponse)
def get_by_id(car_id: str):
    return get_car_by_id(car_id)

@router.patch("/{car_id}", response_model=CarResponse)
def update(car_id: str, data: CarUpdate):
    return update_car(car_id, data)

@router.delete("/{car_id}")
def delete(car_id: str):
    return delete_car(car_id)

app = FastAPI(title="Cars API")
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("crud_carros:app", host="0.0.0.0", port=4000, reload=True)