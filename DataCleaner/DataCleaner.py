import pandas as pd
from Helpers.Logger import get_logger
import re
import math

class DataCleaner:
    def __init__(self,scrapped_data):
        self.logger = get_logger()
        self.scrapped_data = scrapped_data 
        self.df = None
        self.uniques_keys = set()

    def start(self):
        try:
            self.logger.info("Starting data cleaning process")
            if not self.scrapped_data:
                raise ValueError("No data to clean")
            self.to_dataframe()
            self.clear_data()
            self.df.to_csv("output.txt", sep="\t", index=False, encoding="utf-8")
            self.logger.info("Data cleaning process completed")
            return se
        except Exception as e:
            self.logger.error(f"Error in start: {e}")
            raise

    def to_dataframe(self):
        try:
            self.logger.info("Changing data to dataframe")
            data_rows = []
            for item in self.scrapped_data:
                row = {}
                row["url"] = item["url"]
                general_info = item["data"]
                detail_info_list = general_info.pop("details", None)
                row.update(general_info)
                if detail_info_list:
                    detail_info = {detail["offerDetailsKey"]:detail["offerDetailsValue"] for detail in detail_info_list}
                    row.update(detail_info)
                data_rows.append(row)
            self.df = pd.DataFrame(data_rows)
            self.logger.info("Data changed to dataframe")
        except Exception as e:
            self.logger.error(f"Error in to_dataframe: {e}")
            raise
  
    def clear_data(self):
        try:
            self.logger.info("Starting data cleanup")
            if self.df is None:
                raise ValueError("DataFrame is not initialized. Call to_dataframe first.")
            self.df = self.df.map(self.clean_white_marks)
            self.df["price"] = self.df["price"].apply(self.clean_prices)
            self.df["price_m2"] = self.df["price_m2"].apply(self.clean_prices)
            self.df["Powierzchnia:"] = self.df["Powierzchnia:"].apply(self.clean_prices)
            if "Czynsz:" in self.df.columns:
                self.df["Czynsz:"] = self.df["Czynsz:"].apply(self.clean_rent)
            self.df[["street", "neighborhood", "district", "city", "voivodeship"]] = self.df["address"].apply(lambda x: pd.Series(self.split_address(x)))
            if "Dostępne od:" in self.df.columns:
                self.df["Dostępne od:"] = pd.to_datetime(self.df["Dostępne od:"], format="%Y-%m-%d")
            if "Rok budowy:" in self.df.columns:
                self.df["Rok budowy:"] = pd.to_datetime(self.df["Rok budowy:"], format="%Y-%m-%d")
            self.map_to_db_dicts()
            self.logger.info("Data cleanup completed")
        except Exception as e:
            self.logger.error(f"Error in clear_data: {e}")
            raise

    def clean_prices(self, value: str)-> int:
        if isinstance(value, str):
            value = re.sub(r"[^\d]", "", value)
            return int(value) if value.isdigit() else None
        return None
    
    def clean_rent(self, value: str)-> int:
        if isinstance(value, str):
            value = re.sub(r"[^\d]", "", value)
            return value
        return "brak informacji"
    
    def clean_white_marks(self, value: str)->str:
        if isinstance(value, str):
            return re.sub(r"\s+", " ", value).strip()
        return value
    
    def split_address(self, address: str):
        try:
            if isinstance(address, str):
                parts = [part.strip() for part in address.split(",")]
                if len(parts) == 5:
                    street, neighborhood, district, city, voivodeship = parts
                    return street, neighborhood, district, city, voivodeship
                else:
                    neighborhood, district, city, voivodeship = parts
                    return None, neighborhood, district, city, voivodeship
            return [None]*5
        except Exception as e:
            self.logger.error(f"Error in split_address: {e}")
            return [None]*5

    def     map_to_db_dicts(self):
            mapping = {
                "Url": "url",
                "Price": "price",
                "PriceSquare": "price_m2",
                "Address": "address",
                "OfferType": "offerType",
                "Description": "description",
                "Area": "Powierzchnia:",
                "Rooms": "Liczba pokoi:",
                "Heating": "Ogrzewanie:",
                "Floor": "Piętro:",
                "Rent": "Czynsz:",
                "FinishState": "Stan wykończenia:",
                "Market": "Rynek:",
                "Ownership": "Forma własności:",
                "AvailableFrom": "Dostępne od:",
                "AdvertiserType": "Typ ogłoszeniodawcy:",
                "ExtraInfo": "Informacje dodatkowe:",
                "Elevator": "Winda:",
                "BuildingType": "Rodzaj zabudowy:",
                "BuildingMaterial": "Materiał budynku:",
                "Windows": "Okna:",
                "Equipment": "Wyposażenie:",
                "Security": "Zabezpieczenia:",
                "Street": "street",
                "Neighborhood": "neighborhood",
                "District": "district",
                "City": "city",
                "Voivodeship": "voivodeship"
            }
            if self.df is None:
                raise ValueError("DataFrame is not initialized. Call to_dataframe first.")
            result = []
            for _, row in self.df.iterrows():
                obj = {}
                for key, value in mapping.items():
                    if value in self.df.columns:
                        val = row[value]
                        # Sprawdź NaN lub None
                        if val is None or (isinstance(val, float) and math.isnan(val)):
                            obj[key] = "brak informacji"
                        else:
                            obj[key] = val
                    else:
                        obj[key] = "brak informacji"
                result.append(obj)
            return result