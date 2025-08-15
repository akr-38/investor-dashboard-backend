# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, CheckConstraint, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from .database import Base

class Manufacturer(Base):
    __tablename__ = "manufacturers"
    manufacturer_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)

class VehicleCategory(Base):
    __tablename__ = "vehicle_categories"
    category_id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False, index=True)  # '2W','3W','4W'
    __table_args__ = (UniqueConstraint("code", name="uq_vehicle_categories_code"),)

class RegistrationStat(Base):
    __tablename__ = "registration_stats"
    stat_id = Column(Integer, primary_key=True, index=True)
    manufacturer_id = Column(Integer, ForeignKey("manufacturers.manufacturer_id"), nullable=False)
    category_id = Column(Integer, ForeignKey("vehicle_categories.category_id"), nullable=False)
    year = Column(Integer, nullable=False, index=True)
    quarter = Column(Integer, nullable=False, index=True)
    registration_count = Column(Integer, nullable=False)

    manufacturer = relationship("Manufacturer")
    category = relationship("VehicleCategory")

    __table_args__ = (
        CheckConstraint("quarter >= 1 AND quarter <= 4", name="chk_quarter_range"),
        Index("ix_regstats_year_quarter", "year", "quarter"),
        Index("ix_regstats_manu_cat", "manufacturer_id", "category_id"),
    )
