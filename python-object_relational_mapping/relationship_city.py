#!/usr/bin/python3
"""Define the City model using the relationship declarative base."""

from sqlalchemy import Column, ForeignKey, Integer, String
from relationship_state import Base


class City(Base):
    """Represent a city linked to a state."""

    __tablename__ = "cities"

    id = Column(
        Integer,
        primary_key=True,
        nullable=False,
        autoincrement=True
    )
    name = Column(String(128), nullable=False)
    state_id = Column(
        Integer,
        ForeignKey("states.id"),
        nullable=False
    )
