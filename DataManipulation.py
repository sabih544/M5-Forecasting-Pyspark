from pyspark.sql import SparkSession


class DataManipulation:
    def __init__(self):
        self.spark = SparkSession.builder.getOrCreate()

    def read_data(self):
        calendarDf = self.spark.read.option("inferSchema", "true").option("header", "true").csv("./data/calendar.csv")
        modifiedSalesTrainDf = self.spark.read.option("inferSchema", "true").option("header", "true")\
            .csv("./data/modifiedsalesTrainDf.csv")
        sellPricesDf = self.spark.read.option("inferSchema", "true").option("header", "true")\
            .csv("./data/sell_prices.csv")
        return calendarDf, modifiedSalesTrainDf, sellPricesDf

    def get_data(self):
        calendarDf, modifiedSalesTrainDf, sellPricesDf = self.read_data()
        df = modifiedSalesTrainDf.join(calendarDf, modifiedSalesTrainDf.day == calendarDf.d, "left")
        df = df.drop("d")
        df = df.join(sellPricesDf, on=["store_id", "item_id", "wm_yr_wk"], how="left")
        return df

    @staticmethod
    def filter_store(df, store_name):
        return df.filter(df.store_id == store_name)

