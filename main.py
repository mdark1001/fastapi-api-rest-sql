"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 15/03/22
@name: main
"""
import uvicorn as uvicorn
from fastapi import FastAPI

from database.engine import engine, AppModel
from users import router
from credits import routers as credit_router
from database import settings

app = FastAPI(
    title=settings.PROJECT_NAME
)
app.include_router(router.router)
app.include_router(credit_router.router)
# recreate database
# AppModel.metadata.drop_all(engine)
AppModel.metadata.create_all(engine)

if __name__ == '__main__':
    uvicorn.run(app, port=8000)
