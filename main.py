
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

# Абсолютные импорты из вашего пакета app
from app.database import engine, get_db
from app import models, schemas

import warnings
from sqlalchemy.exc import SAWarning

# Отключаем конкретные предупреждения SQLAlchemy
warnings.filterwarnings('ignore', category=SAWarning)

# Создаем таблицы
models.Base.metadata.create_all(bind=engine)

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "Welcome to FastAPI",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }
app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/positions/", response_model=schemas.Position)
def create_position(position: schemas.PositionCreate, db: Session = Depends(get_db)):
    db_position = models.Position(title=position.title)
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    return db_position

@app.get("/positions/", response_model=list[schemas.Position])
def read_positions(db: Session = Depends(get_db)):
    return db.query(models.Position).all()

@app.post("/employees/", response_model=schemas.Employee)
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    db_employee = models.Employee(
        full_name=employee.full_name,
        position_id=employee.position_id
    )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

@app.get("/employees/", response_model=list[schemas.Employee])
def read_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

    from fastapi import Request
    from fastapi.responses import JSONResponse


    @app.exception_handler(404)
    async def not_found_exception_handler(request: Request, exc):
        return JSONResponse(
            status_code=404,
            content={"message": "Endpoint not found"},
        )


    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    import warnings
    from sqlalchemy.exc import SAWarning
    from fastapi import FastAPI, status
    from fastapi.responses import JSONResponse

    # Настройка логирования
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Отключаем warnings SQLAlchemy
    warnings.filterwarnings("ignore", category=SAWarning)

    app = FastAPI(title="My FastAPI Service")


    @app.on_event("startup")
    async def startup():
        logger.info("Service starting...")


    @app.get("/", status_code=status.HTTP_200_OK)
    async def health_check():
        return JSONResponse(
            content={
                "status": "running",
                "endpoints": {
                    "docs": "/docs",
                    "redoc": "/redoc"
                }
            }
        )


    if __name__ == "__main__":
        import uvicorn

        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            log_level="info"
        )

        if __name__ == "__main__":
            import uvicorn

            uvicorn.run(app, host="0.0.0.0", port=8000)

            if __name__ == "__main__":
                import uvicorn

                uvicorn.run(app, host="0.0.0.0", port=8000)