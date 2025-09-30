import pandas as pd
from Helpers.Logger import get_logger

class DataCleaner:
    def __init__(self,scrapped_data):
        self.logger = get_logger()
        self.scrapped_data = scrapped_data 
        self.df = None

    def start(self):
        self.to_dataframe()

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
