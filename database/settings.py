"""
@author: Miguel Cabrera R. <miguel.cabrera@oohel.net>
@date: 15/03/22
@name: settings
"""
SQLALCHEMY_DATABASE_URL = 'sqlite:///./db/api.sqlite3'
PROJECT_NAME = 'Tangelo API USING FASTAPI'
ACCESS_TOKEN_EXPIRE_DAYS = 30
SECRET_KEY = '05cf64558c1a97175e3951ca0407a4b089e6056ff7404cc6618cd39654b06106'
API_VERSION = '/api/v1/'