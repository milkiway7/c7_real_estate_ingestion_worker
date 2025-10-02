from sqlalchemy import Column, Integer, DateTime, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class SecondaryMarketTable(Base):

    __tablename__ = "SecondaryMarket"

    Id = Column(Integer, primary_key=True, autoincrement=True)
    CreatedAt = Column(DateTime, nullable=False)
    UrlAddress = Column(String, nullable=False)
    Price = Column(Integer, nullable=True)
    PriceSquare = Column(Integer, nullable=True)
    Address = Column(String, nullable=True)
    Voivodeship = Column(String, nullable=True)
    City = Column(String, nullable=True)
    District = Column(String, nullable=True)
    Neighbourhood = Column(String, nullable=True)
    Street = Column(String, nullable=True)
    OfferType = Column(String, nullable=True)
    Description = Column(String, nullable=True)
    Equipment = Column(String, nullable=True)
    OfferMaker = Column(String, nullable=True)
    Safety = Column(String, nullable=True)
    BuildingMaterials = Column(String, nullable=True)
    Media = Column(String, nullable=True)
    PropertyType = Column(String, nullable=True)
    Elevator = Column(String, nullable=True)
    Heating = Column(String, nullable=True)
    AdditionalInfo = Column(String, nullable=True)
    DevelopperUrl = Column(String, nullable=True)
    BuildingYear = Column(DateTime, nullable=True)
    Market = Column(String, nullable=True)
    State = Column(String, nullable=True)
    AvailableFrom = Column(DateTime, nullable=True)
    EnergyCertificate = Column(DateTime, nullable=True)
    BuildingType = Column(DateTime, nullable=True)
    Floor = Column(String, nullable=True)
    Rent = Column(Integer, nullable=True)
    Windows = Column(String, nullable=True)
    Area = Column(Integer, nullable=True)
    Rooms = Column(String, nullable=True)




    