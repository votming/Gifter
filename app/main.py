import logging
from logging.handlers import TimedRotatingFileHandler

import uvicorn
from fastapi import FastAPI

from admin.main import AdminAuth
from admin.main import mount_admin_routes
from admin.views.countries import CountryView
from admin.views.titles import TitleView
from app.modules.database import engine
from app.routers import countries, languages, currencies, titles, base, paragraphs
from sqladmin import Admin
from prometheus_fastapi_instrumentator import Instrumentator

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s - %(message)s [%(name)s]",
    datefmt='%Y-%m-%d %H:%M:%S',
    handlers=[
        TimedRotatingFileHandler('logs/logging.log', when='midnight', backupCount=10),
        logging.StreamHandler()
    ]
)

# Start the server
app = FastAPI()


# Connect all backend (FastAPI) routers (APIs)
app.include_router(countries.router, prefix='/api/countries', tags=["countries"])
app.include_router(languages.router, prefix='/api/languages', tags=["languages"])
app.include_router(currencies.router, prefix='/api/currencies', tags=["currencies"])
app.include_router(titles.router, prefix='/api/titles', tags=["titles"])
app.include_router(paragraphs.router, prefix='/api/paragraphs', tags=["paragraphs"])
app.include_router(base.router, prefix='/api', tags=["base"])
Instrumentator().instrument(app).expose(app)

# Create frontend app, connect all frontend (SqlAdmin) views
mount_admin_routes(app)


#if __name__ == "__main__":
#    uvicorn.run(app, host="0.0.0.0", port=8000)
