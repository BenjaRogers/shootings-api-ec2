from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Float
from flask_sqlalchemy import SQLAlchemy

Base = declarative_base()
db = SQLAlchemy()


# Users for API
class Users(Base, db.Model):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    public_id = Column(String(50), unique=True)
    name = Column(String(50))
    password = Column(String(100))
    admin = Column(Boolean)

# V2
class Person(Base, db.Model):
    __tablename__ = "person"
    db_id = Column(Integer(), primary_key=True, index=True)
    id = Column(String(10), unique=True)
    name = Column(String(50), nullable=True)
    date = Column(String(15), nullable=True)
    body_camera = Column(Boolean, nullable=True)
    city = Column(String(50), nullable=True)
    county = Column(String(50), nullable=True)
    state = Column(String(50), nullable=True)
    longitude = Column(Float, nullable=True)
    latitude = Column(Float, nullable=True)
    location_precision = Column(String(50), nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(15), nullable=True)
    race = Column(String(15), nullable=True)
    race_source = Column(String(20), nullable=True)
    was_mental_illness_related = Column(Boolean, nullable=True)
    threat_type = Column(String(20), nullable=True)
    armed_with = Column(String(50), nullable=True)
    flee_status = Column(String(10), nullable=True)
    agency_ids = Column(String(20), nullable=True)

class Agency(Base, db.Model):
    __tablename__ = "agency"
    db_id = Column(Integer(), primary_key=True, index=True)
    id = Column(String(10), unique=True)
    name = Column(String(100), nullable=True)
    type = Column(String(20), nullable=True)
    state = Column(String(5), nullable=True)
    oricodes = Column(String(50), nullable=True)
    total_shootings = Column(Integer, nullable=True)



# Victims of PV V1
# class Person(Base, db.Model):
#     __tablename__ = "person"
#     db_id = Column(Integer(), primary_key=True, index=True)
#     id = Column(String(10), unique=True)
#     name = Column(String(50), nullable=True)
#     date = Column(String(15), nullable=True)
#     manner_of_death = Column(String(50), nullable=True)
#     armed = Column(String(50), nullable=True)
#     age = Column(Float, nullable=True)
#     gender = Column(String(5), nullable=True)
#     race = Column(String(5), nullable=True)
#     city = Column(String(50), nullable=True)
#     state = Column(String(50), nullable=True)
#     signs_of_mental_illness = Column(Boolean, nullable=True)
#     threat_level = Column(String(50), nullable=True)
#     flee = Column(String(50), nullable=True)
#     body_camera = Column(Boolean, nullable=True)
#     longitude = Column(Float, nullable=True)
#     latitude = Column(Float, nullable=True)
#     is_geocoding_exact = Column(Boolean, nullable=True)
