# Databricks notebook source
from pyspark.sql.functions import datediff, current_date
from pyspark.sql.types import IntegerType
from pyspark.sql.functions import avg

# COMMAND ----------

# MAGIC %md #### Read in Dataset

# COMMAND ----------

df_laptimes = spark.read.csv('s3://columbia-gr5069-main/raw/lap_times.csv', header=True)

# COMMAND ----------

df_drivers = spark.read.csv('s3://columbia-gr5069-main/raw/drivers.csv', header=True)

# COMMAND ----------

df_races = spark.read.csv('s3://columbia-gr5069-main/raw/races.csv', header=True)

# COMMAND ----------

display(df_drivers)

# COMMAND ----------

# MAGIC %md #### Transform Data

# COMMAND ----------

df_drivers = df_drivers.withColumn('age', datediff(current_date(), df_drivers.dob)/365)

# COMMAND ----------

display(df_drivers)

# COMMAND ----------

df_drivers =  df_drivers.withColumn('age', df_drivers['age'].cast(IntegerType()))

# COMMAND ----------

df_lap_drivers = df_drivers.join(df_laptimes, on='driverId')

# COMMAND ----------



# COMMAND ----------

df_lap_drivers = df_drivers.select('driverId','driverRef', 'code', 'forename', 'surname', 'nationality', 'age').join(df_laptimes, on=['driverId'])

# COMMAND ----------

display(df_lap_drivers)

# COMMAND ----------

df_lap_drivers = df_lap_drivers.join(df_races.select('name', 'year', 'raceId'), on=['raceId'])

# COMMAND ----------

display(df_lap_drivers)

# COMMAND ----------

# MAGIC %md #### Aggregate by Age

# COMMAND ----------

df_agg_age = df_lap_drivers.groupby('age').agg(avg('milliseconds'))

# COMMAND ----------

df_agg_age.write.csv('s3://ih2400-gr5069/processed/inclass/laptimes_by_age.csv')

# COMMAND ----------


