from datetime import datetime
from typing import List
from pydantic import BaseModel, Field


class ParagraphBaseSchema(BaseModel):
    template: str
    language_id: int
    country_id: int | None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class TitleBaseSchema(BaseModel):
    template: str
    gender: str | None = Field(max_length=10)
    language_id: int
    country_id: int | None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class CurrencyBaseSchema(BaseModel):
    name: str
    name_en: str
    code: str = Field(max_length=5)
    symbol: str = Field(max_length=5)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class CountryBaseSchema(BaseModel):
    name: str
    code: str = Field(max_length=2)
    demonym: str
    demonym_plural: str
    bank_name: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListCountryResponse(BaseModel):
    status: str
    results: int
    notes: List[CountryBaseSchema]


class LanguageBaseSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class ListLanguageResponse(BaseModel):
    status: str
    results: int
    notes: List[LanguageBaseSchema]
