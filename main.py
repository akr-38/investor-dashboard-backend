from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.database import engine, get_db
from app import models
from pydantic import BaseModel
from sqlalchemy import func


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Details(BaseModel):
    category: str
    manufacturer: str
    start_year: int
    start_quarter: int
    end_year: int
    end_quarter: int


@app.post("/all_categories_all_manufacturers")
def all_categories_all_manufacturers(details: Details, db: Session = Depends(get_db)):
    # Aggregate sum of registration_count per year and quarter
    results = (
        db.query(
            models.RegistrationStat.year,
            models.RegistrationStat.quarter,
            func.sum(models.RegistrationStat.registration_count).label("total_registrations")
        )
        .filter(
            # Filter by start and end year & quarter
            (models.RegistrationStat.year > details.start_year) |
            ((models.RegistrationStat.year == details.start_year) &
             (models.RegistrationStat.quarter >= details.start_quarter)),
            (models.RegistrationStat.year < details.end_year) |
            ((models.RegistrationStat.year == details.end_year) &
             (models.RegistrationStat.quarter <= details.end_quarter))
        )
        .group_by(models.RegistrationStat.year, models.RegistrationStat.quarter)
        .order_by(models.RegistrationStat.year, models.RegistrationStat.quarter)
        .all()
    )

    # Convert to list of dicts
    response = [
        {"year": r.year, "quarter": r.quarter, "total_registrations": r.total_registrations}
        for r in results
    ]

    return {"data": response}


from sqlalchemy import func
from fastapi import Depends
from sqlalchemy.orm import Session

@app.post("/all_categories_specific_manufacturer")
def all_categories_specific_manufacturer(details: Details, db: Session = Depends(get_db)):
    # Find the manufacturer ID
    manufacturer_obj = db.query(models.Manufacturer).filter(
        models.Manufacturer.name == details.manufacturer
    ).first()
    
    if not manufacturer_obj:
        return {"error": f"Manufacturer '{details.manufacturer}' not found"}
    
    # Query RegistrationStat for this manufacturer, sum across all categories
    results = (
        db.query(
            models.RegistrationStat.year,
            models.RegistrationStat.quarter,
            func.sum(models.RegistrationStat.registration_count).label("total_registrations")
        )
        .filter(
            models.RegistrationStat.manufacturer_id == manufacturer_obj.manufacturer_id,
            models.RegistrationStat.year >= details.start_year,
            models.RegistrationStat.year <= details.end_year,
            ((models.RegistrationStat.year > details.start_year) |
             ((models.RegistrationStat.year == details.start_year) &
              (models.RegistrationStat.quarter >= details.start_quarter))),
            ((models.RegistrationStat.year < details.end_year) |
             ((models.RegistrationStat.year == details.end_year) &
              (models.RegistrationStat.quarter <= details.end_quarter)))
        )
        .group_by(models.RegistrationStat.year, models.RegistrationStat.quarter)
        .order_by(models.RegistrationStat.year, models.RegistrationStat.quarter)
        .all()
    )

    response = [
        {"year": r.year, "quarter": r.quarter, "registration_count": r.total_registrations}
        for r in results
    ]

    return {"data": response}


from sqlalchemy import func
from fastapi import Depends
from sqlalchemy.orm import Session

@app.post("/specific_category_all_manufacturers")
def specific_category_all_manufacturers(details: Details, db: Session = Depends(get_db)):
    # Find the category ID
    category_obj = db.query(models.VehicleCategory).filter(
        models.VehicleCategory.code == details.category
    ).first()
    
    if not category_obj:
        return {"error": f"Category '{details.category}' not found"}
    
    # Query RegistrationStat for this category, sum across all manufacturers
    results = (
        db.query(
            models.RegistrationStat.year,
            models.RegistrationStat.quarter,
            func.sum(models.RegistrationStat.registration_count).label("total_registrations")
        )
        .filter(
            models.RegistrationStat.category_id == category_obj.category_id,
            models.RegistrationStat.year >= details.start_year,
            models.RegistrationStat.year <= details.end_year,
            ((models.RegistrationStat.year > details.start_year) |
             ((models.RegistrationStat.year == details.start_year) &
              (models.RegistrationStat.quarter >= details.start_quarter))),
            ((models.RegistrationStat.year < details.end_year) |
             ((models.RegistrationStat.year == details.end_year) &
              (models.RegistrationStat.quarter <= details.end_quarter)))
        )
        .group_by(models.RegistrationStat.year, models.RegistrationStat.quarter)
        .order_by(models.RegistrationStat.year, models.RegistrationStat.quarter)
        .all()
    )

    response = [
        {"year": r.year, "quarter": r.quarter, "registration_count": r.total_registrations}
        for r in results
    ]

    return {"data": response}


@app.post("/specific_category_specific_manufacturer")
def specific_category_specific_manufacturer(details: Details, db: Session = Depends(get_db)):
    # Find the category ID
    category_obj = db.query(models.VehicleCategory).filter(
        models.VehicleCategory.code == details.category
    ).first()
    if not category_obj:
        return {"error": f"Category '{details.category}' not found"}

    # Find the manufacturer ID
    manufacturer_obj = db.query(models.Manufacturer).filter(
        models.Manufacturer.name == details.manufacturer
    ).first()
    if not manufacturer_obj:
        return {"error": f"Manufacturer '{details.manufacturer}' not found"}

    # Query RegistrationStat for specific category and specific manufacturer
    results = (
    db.query(
        models.RegistrationStat.year,
        models.RegistrationStat.quarter,
        models.RegistrationStat.registration_count
    )
    .filter(
        models.RegistrationStat.category_id == category_obj.category_id,
        models.RegistrationStat.manufacturer_id == manufacturer_obj.manufacturer_id,
        models.RegistrationStat.year >= details.start_year,
        models.RegistrationStat.year <= details.end_year,
        ((models.RegistrationStat.year > details.start_year) |
         ((models.RegistrationStat.year == details.start_year) &
          (models.RegistrationStat.quarter >= details.start_quarter))),
        ((models.RegistrationStat.year < details.end_year) |
         ((models.RegistrationStat.year == details.end_year) &
          (models.RegistrationStat.quarter <= details.end_quarter)))
    )
    .order_by(models.RegistrationStat.year, models.RegistrationStat.quarter)
    .all()
)


    response = [
        {"year": r.year, "quarter": r.quarter, "registration_count": r.registration_count}
        for r in results
    ]

    return {"data": response}
