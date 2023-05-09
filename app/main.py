from fastapi import FastAPI
from routers import countries, languages, currencies, titles, base, paragraphs

app = FastAPI()
app.include_router(countries.router, prefix='/api/countries', tags=["countries"])
app.include_router(languages.router, prefix='/api/languages', tags=["languages"])
app.include_router(currencies.router, prefix='/api/currencies', tags=["currencies"])
app.include_router(titles.router, prefix='/api/titles', tags=["titles"])
app.include_router(paragraphs.router, prefix='/api/paragraphs', tags=["paragraphs"])
app.include_router(base.router, prefix='/api', tags=["base"])
