from sqlalchemy.orm import Mapped, mapped_column
from ..db import db

class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    description: Mapped[str]
    size_dia_km: Mapped[int]

    def to_dict(self):
        return dict(
            id=self.id,
            name=self.name,
            description=self.description,
            size_dia_km=self.size_dia_km
        )
    
    @classmethod
    def from_dict(cls, planet_data):
        new_planet = cls(
            name=planet_data["name"],
            description=planet_data["description"],
            size_dia_km=planet_data["size_dia_km"]
        )
        return new_planet