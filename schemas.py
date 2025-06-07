from pydantic import BaseModel, Field, validator
from typing import Optional


class PositionBase(BaseModel):
    title: str = Field(..., min_length=2, max_length=100, example="Разработчик")


class PositionCreate(PositionBase):
    pass


class Position(PositionBase):
    id: int = Field(..., example=1)

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "Старший разработчик"
            }
        }


class EmployeeBase(BaseModel):
    full_name: str = Field(
        ...,
        min_length=5,
        max_length=150,
        example="Иванов Иван Иванович",
        description="Полное ФИО сотрудника"
    )

    @validator('full_name')
    def validate_full_name(cls, v):
        parts = v.strip().split()
        if len(parts) < 2:
            raise ValueError("Должно содержать минимум фамилию и имя")
        return ' '.join(parts)


class EmployeeCreate(EmployeeBase):
    position_id: int = Field(..., gt=0, example=1)


class Employee(EmployeeBase):
    id: int = Field(..., example=1)
    position_id: int = Field(..., gt=0, example=1)

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "full_name": "Петров Петр Петрович",
                "position_id": 2
            }
        }