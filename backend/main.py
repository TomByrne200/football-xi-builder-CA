from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine, SessionLocal
import models
import schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(title = "Football XI Builder API")

app.add_middleware(
    CORSMiddleware, 
    allow_origins = ["http://localhost:5173","http://127.0.0.1:5173"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return{"message": "Football XI Builder API is working!"}

@app.post("/players", response_model=schemas.Player)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    db_player = models.Player(
        player_name = player.player_name,
        player_number = player.player_number,
        position = player.position,
        on_starting_xi = False
    )

    db.add(db_player)
    db.commit()
    db.refresh(db_player)

    return db_player

@app.get("/players", response_model=list[schemas.Player])
def get_players(db: Session = Depends(get_db)):
    players = db.query(models.Player).all()

    return players

@app.get("/players/{player_id}",response_model = schemas.Player)
def get_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()

    if player is None:
        raise HTTPException(status_code=404, detail = "Player not found")

    return player

@app.put("/players/{player_id}", response_model = schemas.Player)
def update_player(player_id: int, updated_player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()

    if player is None:
        raise HTTPException(status_code=404, detail="Player not found")

    player.player_name = updated_player.player_name
    player.player_number = updated_player.player_number
    player.position = updated_player.position

    db.commit()
    db.refresh(player)

    return player

@app.delete("/players/{player_id}")
def delete_player(player_id: int, db: Session = Depends(get_db)):
    player = db.query(models.Player).filter(models.Player.id == player_id).first()

    if player is None:
        raise HTTPException(status_code = 404, detail = "Player not found")
        
    db.delete(player)
    db.commit()

    return {"message": "Player deleted sucessfully"}