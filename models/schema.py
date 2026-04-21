from pydantic import BaseModel, Field
from typing import List, Optional, Literal

class Patient(BaseModel):
    age: Optional[int]
    sex: Optional[Literal["male", "female"]]


class ClinicalData(BaseModel):
    patient: Patient
    diagnosis: Optional[str] = Field(None, min_length=3)
    findings: List[str]
    treatment: Optional[str] = Field(None, min_length=3)