from sqlalchemy import Boolean, Column, Integer, String

from database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    player_name = Column(String, nullable= False)
    player_number = Column(Integer, nullable = False)
    position = Column(String, nullable = False)
    on_starting_xi = Column(Boolean, default=False)