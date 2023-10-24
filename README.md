# LATAM CHALLENGE

## Resolución
Se solicitó resolver 3 ejercicios:
1. Top 10 de fechas donde hubo mayor actividad y el usuario que más actividad tuvo en dichas fechas.
2. Top 10 de emojis.
3. Top 10 de usuarios según menciones.

- En la carpeta src se encuentra cada resolución. 
- Tanto para el ejercicio 1 como para el 3 el desarrollo fue sobre q1_memory y q3_memory respectivamente
dado que se eligió como framework de trabajo spark. El mismo tiene funciones internas las mismas están optimizadas 
para ejecución por eso en esta ocasión me pareció redundante copiar el script en ambas secciones.
- En el caso del ejercicio 2, se realizaron 2 scripts, divididos en q2_memory y q2_time. En ambos se trabajó con el spark,
pero la particularidad es el el uso de una librería externa basada en itertools, que optimiza el correcto scrapping de los 
unicodes generando con muchísima precisión un filtro por todos los emojis válidos, caracterizándolos por grupos de emojis y
contemplando todos los skins tones. La desventaja de esta librería es el tiempo de ejecución, sobrepasando los 4 min para
la ejecución de este script. 
Optimizando el ejercicio 2 en tiempo, se utilizó la librería re, para filtrar por un patrón de unicode que representara
los rangos de emojis según categoría. El tiempo de ejecución disminuyó drásticamente mediante esta resolución, llegando
a tardar unos 6~8 segundos en retornar el output.

## Ejecución del código

Para ejecutar el código en tiempo real, basta con entrar a una notebook de [Google Colab](https://colab.new/)
1. Si pide loguearse, se realiza mediante las credenciales de cualquier cuenta de Gsuite o Gmail
2. En la parte izquierda de la página encontramos un ícono de carpeta (recuadro amarillo), haciendo click ahí podremos ver los archivos que existen para nuestro entorno de trabajo. Debemos arrastrar allí el archivo formato JSON que obtenemos de descomprimir el [siguiente archivo](https://drive.google.com/file/d/1ig2ngoXFTxP5Pa8muXo02mDTFexZzsis/view?usp=sharing).
3. El otro archivo que deberíamos arrastar es el requirements.txt contenido en este repositorio.
4. Para instalar las dependencias en la celda de código (recuadro rojo) ejecutaremos el siguiente comando:
    - !pip install -r /content/requirements.txt
5. Una vez instalado los requerimientos generaremos la variable de file_path de la siguiente manera:
    - file_path = 'farmers-protest-tweets-2021-2-4.json'
6. Debería quedar de la siguiente manera:
    - ![Colab](https://imgtr.ee/images/2023/10/24/c106cf1389a6ea04d0f93067d840df10.png)

## Mejoras

1. Pensaría en el ciclo de vida del dato desde la ingesta hasta la disponibilización final.
Una arquitectura orientada a un ELT, mediante eventos u orquestada con un componente como [airflow](https://airflow.apache.org/docs/apache-airflow/stable/index.html), [mage](https://docs.mage.ai/introduction/overview), [meltano](https://docs.meltano.com/?_gl=1*10nwiik*_gcl_au*MTQ3NjMwNTkyOC4xNjk4MTE5ODA2). Optimizando y entendiendo las necesidades y requerimientos del stakeholder.
2. Pensaría en almacenar ciertas capas de información. Una primera donde esté el archivo en crudo en su formato de origen, luego una capa con un tratamiento mínimo, tal vez tratamiento de nulos y duplicados, tipo de formato parquet o AVRO, facilitando su compresión y posterior almacenamiento particionado que optimizaría el procesamiento en paralelo mediante spark, beam, flink.
3. Puntualmente en el caso 2, pensaría con que grado de confianza y en qué tiempo se necesita el procesamiento del texto para extracción de emojis. Si es una cuestión de sentimental análisis, probablemente sea mucha más importante la precisión que el tiempo de ejecución. A su vez para lograr mejor precisión y menor tiempo de ejecución, debería trabajar en optimizar el patrón de expresión regular para que diferencie y capte mejor cada uno de los unicode. Si bien me basé para el patrón en la documentación de X, al compilar la expresión regular, surgieron varios problemas que interrumpieron la ejecución del script.

## Arquitectura Open Source
![imagen](https://imgtr.ee/images/2023/10/24/3fcc1c38524a7343684b77d78dd19926.png)
1. Podríamos explorar conectores de meltano para extrar data e ingestarla en un hdfs contenerizado, desde el cuál se pueda usar un orquestador y herramienta de procesamiento como lo es spark
2. Pensando en un tipo de ingesta en tiempo real, podríamos implementar un sistema de mensajes al estilo kafka, pensando en las diferentes puntos de dolor de las arquitecturas Kappa y Lambda.
3. Disponibilización a herramientas de BI para generar reportes y o métricas.
4. Se podría organizar un sistema de logs y alertas con elasticsearch, o utilizando componentes de airflow como el slack operator, enviado notificaciones antes diferentes tresholes. 

## Arquitectura Cloud
![cloud-arqui](https://imgtr.ee/images/2023/10/24/4701ac75b9400c34bb038084293b9ec2.png)
1. Pensando en una arquitectura cloud en GCP, me gusta pensar en como la data se mantiene securitizada en tránsito y en reposo. Generaría un landing zone, donde pueda alojar la data que quiero procesar aplicando políticas de life cycle management para abaratar costos. 
2. Generaría una división en el landing zone donde guardaría un archivo que contenga mínimas transformaciones sobre el crudo y compresión a un formato de mayor ventaja para el procesamiento, como AVRO / parquet
3. Una vez escribo en este bucket, mediante un sensor de composer, cloud functions, despertaría un procesamiento de datos en las herramientas de analítica, dataflow o dataproc. Si dentro de los requerimientos existe la necesidad de una ingesta en tiempo real, me inclinaría por pub/sub y dataflow.
4. Guardaría los datos procesados y particionados en un bucket de curado, donde podría hacer analítica descriptiva y avanzada.
5. Tendría una conexión con Looker Studio o una herramienta de BI para reportería.
6. En loggeo y monitoreo con alertas, se puede desarrollar con las herramientas in house como cloud logging y monitoring.
7. A su vez contamos con la gran utilidad de control de accesos mediante Cloud IAM, como también la posibilidad de crear cuentas de servicio que personifiquen servicios, siguiendo las buenas prácticas recomendadas por Google, aplicando el principio de menor privilegio y grupos de usuarios a quienes asignar roles y permisos. Sin mencionar la facilidad de imitar la organización mediante la estructura de carpetas y proyectos dentro de GCP.