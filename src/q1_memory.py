from typing import List, Tuple
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as F

spark = SparkSession \
    .builder \
    .appName("Latamchallenge") \
    .getOrCreate()

def q1_memory(file_path: str) -> List[Tuple[datetime.date, str]]:
    '''
    Función para transformación y solución análitica con el fin de obtener
    las 10 fechas en las que más actividad hubo en la plataforma de X a su vez
    de reconocer en cada fecha quién fue el usuario que más tweets realizó.
    '''

    # Generación de un dataframe de data cruda
    rdata = spark.read.json(file_path)

    # Filtro la data cruda quedándome sólo con las columnas que necesito para este problema.
    q1_data = rdata.select('date', 'user.username').withColumn("date", F.to_date('date'))
    
    # Realizo un conteo por fecha y por usuario.
    # Me servirá para luego sacar los top10 por fecha y por usuario
    date_activity = q1_data.groupBy('date', 'username').count()

    # Realizo una sumarización del conteo por fecha
    date_total_activity = date_activity.groupBy('date').agg(F.sum('count').alias('total_activity'))

    # Mediante la función analítica genero un ranking de la actividad por día
    window_spec = Window.orderBy(F.desc("total_activity"))
    date_total_activity = date_total_activity.withColumn("rank", F.row_number().over(window_spec))

    # Realizo un filtro por la columna ranking quedándome sólo con las menores o iguales a 10
    top_10_dates = date_total_activity.filter("rank <= 10")

    # Utilizo la misma función analítica row_number, en esta ocasión para filtrar
    # por el usuario que más tweets realizó por cada fecha
    most_active_users_per_date = date_activity \
        .groupBy("date", "username") \
        .agg(F.sum("count").alias("user_activity")) \
        .withColumn("rank", F.row_number().over(Window.partitionBy("date").orderBy(F.desc("user_activity")))) \
        .filter("rank = 1")

    # Realizo un join, respetando el orden de mi top10 de fechas con más actividad
    # mencionando al usuario que más tweets realizó en cada fecha
    # devuelvo el elemento como una lista de tuplas con los tipos de datos solicitados por la función

    return top_10_dates.join(most_active_users_per_date, on=['date'], how='left').select('date', 'username').collect()