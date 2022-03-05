import json
from kafka import KafkaProducer
from pyspark.sql import SparkSession
import time
from pyspark.sql.types import IntegerType, TimestampType, StringType
from pyspark.sql.functions import *
import os


MALDATA = os.environ['MALWER_DATA']

#Method for initialize spark.
def init():
    spark = SparkSession.builder.appName('AndroidMalwareProducer').master("spark://spark-master:7077").getOrCreate()
    return spark
#Method for parsing data from file.
#@param: inputhPath Path to the file.
#@param: spark SparkSession.  
 
def parsingData(inputPath, spark):
    df = spark.read.options(header='True').csv(inputPath)
    df2 = df.withColumn(" Timestamp", to_timestamp(col(" Timestamp"), 'dd/MM/yyyy HH:mm:ss'))
    df3 = df2.withColumn(" Timestamp", df2[" Timestamp"].cast(StringType())) 
    return df3
    
# Create producer
producer = KafkaProducer(
    bootstrap_servers='kafka-server:9092', 
    value_serializer=lambda v: json.dumps(v).encode('utf-8'))

# Read streaming event
sc = init()
data = parsingData(MALDATA, sc)

clearData = data[" Source IP"," Source Port"," Destination IP", " Destination Port"," Timestamp"," Flow Duration"," Total Fwd Packets"," Total Backward Packets","Total Length of Fwd Packets"," Total Length of Bwd Packets","Flow Bytes/s"," Flow Packets/s"]
rdd2 = clearData.rdd.map(lambda x: [clearData for clearData in x])
mesData = rdd2.collect()

for msg in mesData:
    m = str(msg)
    m = m[1:-1]
    m = m.replace("'", "")
    producer.send('AndMalwer',m)
    print(m)
    time.sleep(3)