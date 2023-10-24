from typing import List, Tuple
import re
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as F

spark = SparkSession \
    .builder \
    .appName("Latamchallenge") \
    .getOrCreate()

def q2_time(file_path: str) -> List[Tuple[str, int]]:
    '''
    Función para transformación y solución análitica con el fin de obtener
    las 10 emojis más usados y su conteo en la plataforma de X.
    '''

    # patron de expresion regular para filtrar unicodes de emojis
    re = r'([\x{1F600}-\x{1F64F}\x{1F300}-\x{1F5FF}\x{1F680}-\x{1F6FF}\x{1F700}-\x{1F77F}\x{1F780}-\x{1F7FF}\x{1F800}-\x{1F8FF}\x{1F900}-\x{1F9FF}\x{1FA00}-\x{1FA6F}\x{1FA70}-\x{1FAFF}\x{1F004}\x{1F0CF}\x{1F170}-\x{1F251}\x{1F004}-\x{1F251}])|([\x{1F3FB}-\x{1F3FF}])'

    # Generación de un dataframe de data cruda
    rdata = spark.read.json(file_path)

    # Para optimización de memoria, elijo sólo la columna con la que deseo quedarme
    q2_df = rdata.select('content')

    # mediante expresión regular genero una columna emojis, filtrando el contenido por la regex
    df2_emojis = q2_df.withColumn("emojis", F.regexp_extract(F.col("content"), re, 0))

    # filtro el dataframe por las columnas que contienen emojis
    tweets_with_emojis = df2_emojis.filter(F.col("emojis") != "")

    # Conteo de ocurrencias de cada emoji, los ordeno de mayor a menor y limito a 10 ocurrencias para generar el top10
    emoji_counts = tweets_with_emojis.groupBy("emojis").agg(F.count("*").alias("count")).orderBy(F.desc('count')).limit(10)

    # Show the emoji counts
    emojis = emoji_counts.rdd.map(lambda row: (row['emojis'], row['count'])).collect()

    return emojis