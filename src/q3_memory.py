from typing import List, Tuple
from datetime import datetime
from pyspark.sql import SparkSession
from pyspark.sql.window import Window
import pyspark.sql.functions as F


spark = SparkSession \
    .builder \
    .appName("Latamchallenge") \
    .getOrCreate()

def q3_memory(file_path: str) -> List[Tuple[str, int]]:

    '''Función para transformación y solución análitica con el fin de obtener
    las 10 usuarios más influyentes en función del conteo de menciones.
    '''

    # Generación de un dataframe de data cruda
    rdata = spark.read.json(file_path)
    
    # Filtro por las columnas que necesito para este problema
    q3_data = rdata.select('mentionedUsers.username')
    
    # Encuentro que tengo un DataFrame del tipo array<string>
    # que a su vez tiene datos nullos. Elimino los nulos.
    df_filtered = q3_data.filter(col("username").isNotNull())

    # Necesito separar los strings dentro de los arrays
    # para luego contar las ocurrencias.
    exploded_df = df_filtered.select(explode(df_filtered.username).alias("username"))\
        .groupBy("username").agg(count("*").alias("count")).orderBy(F.desc('count')).limit(10)

    data_tuples = exploded_df.rdd.map(lambda row: (row['username'], row['count'])).collect()

    return data_tuples

