Visualizing KSQL Streaming Queries Against Kafka Using Instadeq
---------------------------------------------------------------

Taking this confluent tutorial as a basis, let's go one step further and visualize the streaming queries made with KSQL:

[https://docs.confluent.io/current/ksql/docs/tutorials/basics-docker.html](https://docs.confluent.io/current/ksql/docs/tutorials/basics-docker.html)

We have taken the idea and queries from the ksql tutorial using docker and modified it just a little to make it work with Instadeq. For more details about KSQL follow the Confluent's article.

Requirements
************

1. Create an account in [Instadeq](https://instadeq.com) ![Instadeq](instadeq.png?raw=true "Instadeq") 

2. Install docker in your computer

3. Install python libraries: requests and kafka-python

```
pip install kafka-python

pip install requests
```

4.  You might also need to append kafka to your /etc/hosts file so the script python can solve the Kafka Docker address:

```
vim /etc/hosts

127.0.0.1 kafka
```

Steps
*****

1. Clone this tutorial repo

```
git clone https://github.com/instadeq/ksql-to-instadeq
```


2. Start Zookeeper, Kafka and KSQL server docker containers:


```
cd ksql-to-instadeq
sudo docker-compose up
```


3. Start python data generator. It will publish msgs like *{"ts": 1537153204.0, "username": "javier", "val": 50}* in a Kafka Topic called 'users'.

```
python datagen.py
```


4. From the host machine, start KSQL CLI

```
sudo docker run --network ksqltoinstadeq_net --interactive --tty
    confluentinc/cp-ksql-cli:5.0.0 http://ksql-server:8088
```


5. Run the following queries to create streaming queries against Kafka using KSQL. Check the Confluent tutorial for more information about creating TABLES and STREAMS from Kafka Topics using KSQL.

```
CREATE STREAM users_stream (ts BIGINT, username VARCHAR, val INT) WITH (KAFKA_TOPIC='users', VALUE_FORMAT='JSON', TIMESTAMP='ts');
```

```
CREATE TABLE total_by_username WITH (VALUE_FORMAT='json') AS SELECT username, count(*) AS total
    FROM users_stream
    WINDOW TUMBLING (size 10 minute)
    GROUP BY username
```


6. Execute this python script (or create your own from any other language) to consume *total_by_username* topic and send it to Instadeq

```
python kafka_to_instadeq.py instadeq_username instadeq_password TOTAL_BY_USERNAME total-by-username
```



7. Subscribe to total-by-username channel in Instadeq

![Subscribe](screenshots/subscribe-to-channel.png?raw=true "Subscribe")



8. Visualize your total_by_username KSQL table.

![Visualize](screenshots/visualize-ksql.png?raw=true "Visualize")
