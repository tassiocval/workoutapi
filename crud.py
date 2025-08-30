from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from models import Atleta
from schemas import AtletaCreate

def criar_atleta(db: Session, atleta: AtletaCreate):
    novo_atleta = Atleta(**atleta.dict())
    db.add(novo_atleta)
    try:
        db.commit()
        db.refresh(novo_atleta)
        return novo_atleta
    except IntegrityError:
        db.rollback()
        raise ValueError(f"Já existe um atleta cadastrado com o cpf: {atleta.cpf}")

