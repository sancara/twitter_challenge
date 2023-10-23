from typing import List, Tuple
from pyspark.sql import SparkSession
import advertools as adv

spark = SparkSession \
    .builder \
    .appName("Latamchallenge") \
    .getOrCreate()

def q2_memory(file_path: str) -> List[Tuple[str, int]]:

    '''Función para transformación y solución análitica con el fin de obtener
    las 10 emojis que más se han usado con su respectivo conteo en el set de datos,
    que se nos proporciona
    '''

    # Generación de un dataframe de data cruda
    rdata = spark.read.json(file_path)

    # Selecciono solo la data que necesito
    q2_data = rdata.select('content')

    # Obtener una lista con todos los tweets
    tweets = q2_data.select(q2_data.content).rdd.map(lambda x: x[0]).collect()

    # Utilizo la librería advertools y la función extract_emoji
    content_list = adv.extract_emoji(tweets)

    # Utilizo el output anterior como input y retorno una lista de tuplas
    # conteniendo el emoji y la cantidad de veces que fue usado.
    
    return content_list['top_emoji'][:10]

    