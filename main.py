from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi_pagination import Page, add_pagination, paginate
from database import Base, engine, get_db
import models, schemas, crud

# Cria tabelas se não existirem
Base.metadata.create_all(bind=engine)

app = FastAPI(title="WorkoutAPI")

# ---------------------------
# Endpoint: criar atleta
# ---------------------------
@app.post("/atletas/", response_model=schemas.AtletaRead)
def criar_atleta(atleta: schemas.AtletaCreate, db: Session = Depends(get_db)):
    try:
        return crud.criar_atleta(db, atleta)
    except ValueError as e:
        raise HTTPException(status_code=303, detail=str(e))

# ---------------------------
# Endpoint: listar atletas com filtros e paginação
# ---------------------------
@app.get("/atletas/", response_model=Page[schemas.AtletaRead])
def listar_atletas(
    nome: str | None = Query(None, description="Filtra pelo nome do atleta"),
    cpf: str | None = Query(None, description="Filtra pelo CPF do atleta"),
    skip: int = Query(0, ge=0, description="Número de registros para pular"),
    limit: int = Query(10, ge=1, le=100, description="Número máximo de registros retornados"),
    db: Session = Depends(get_db)
):
    query = db.query(models.Atleta)
    if nome:
        query = query.filter(models.Atleta.nome.ilike(f"%{nome}%"))
    if cpf:
        query = query.filter(models.Atleta.cpf == cpf)
    
    atletas = query.offset(skip).limit(limit).all()
    return paginate(atletas)

# Adiciona paginação global
add_pagination(app)
