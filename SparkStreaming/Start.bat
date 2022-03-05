docker-compose up -d --build namenode datanode spark-master spark-worker-1 spark-worker-2 zookeeper-server kafka-server neo4j App
docker exec -it namenode ./init.sh

docker-compose up -d --build Producer 