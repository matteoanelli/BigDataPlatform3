# Assignment Assignment_3 - Streaming analytics platform

---------------------------------------------------------------------------

This assignment is part of a collection of 3 assignment of the Big Data Platform course at Aalto University.
* [Assignment 1](https://github.com/matteoanelli/BigDataPlatform) : Design of a big data platform (Main components). [Report](https://github.com/matteoanelli/BigDataPlatform/blob/master/assignment-1-801979-master/reports/Report.md)
* [Assignment 2](https://github.com/matteoanelli/BigDataPlatform2) : Data Ingestion [Report](https://github.com/matteoanelli/BigDataPlatform2/blob/master/assignment-2-801979/reports/Report.md)
* [Assignment 3](https://github.com/matteoanelli/BigDataPlatform3) : Analytics [Report](https://github.com/matteoanelli/BigDataPlatform3/blob/master/assignment-3/reports/Report.md)


The [Report](https://github.com/matteoanelli/BigDataPlatform3/blob/master/assignment-3/reports/Report.md) is a full explanation of the project.

### Implemented only the streaming analytics!

---------------------------------------------------------------------------

Inside the following folder the final report with the description of the project can be found.
```
assignment-3-801979/reports
```
The project have been developed in python and Java. Be sure to use version 3.6+ and Java 8+. Furthermore, Maven should be installed as well as Apache Flink 1.9.1+.

Moreover, an environment variable CLOUDAMQP_URL should be set to the CloudAMQP service link connection. As other option, the rabbitMQ can be run locally. This guide assume that the CloudAMQP is used.

The first step is to download the dataset from [NYC taxi Dataset](https://data.cityofnewyork.us/Transportation/2018-Yellow-Taxi-Trip-Data/t29m-gskq).
The dataset has been renamed and it has to be placed inside the data directory as follow:
```
assignment-3-801979/data/2018_Yellow_Taxi.csv
```
Moreover, the header should be removed before start processing it.

As second step all the requirement can be imported.
```
pip install -r requirements.txt
```
To remark the fact that for testing the time of the tumbling window should be reduced of the expected value of 1 hour.
This step is already implemented inside the code setting the time window at 1 second. During the testing this 
parameter can easily be changed. The __timeWindow(Time.seconds(1)__ at line 96 inside the CustomerStreamApp1.java can 
be set at will.

Now the customerstream app can be compiled. It can be found at the following directory:

```
 assignment-3-801979/code/customerstreamapp

```
The first step is to generate the Jar file using maven. It should be done in the directory of the __pom.xml__
```
mvn clean install
```
After that, Flink should be activated. It can be done from the flink-1.9.1/bin directory using the following command:
```
flink start-cluster.sh
```
Once the cluster is activated, the application can be launched as follow:

```
./bin/flink run -p 1 <path_to_CustomerStreamApp.jar>
```
Furthermore, the two python scripts (customer and producer has to be launched) as follow:

```
python assignment-3-801979/code/realtime_ingestion/customer1consumer.py

python assignment-3-801979/code/realtime_ingestion/customer1producer.py
```

Now, the environment is set up and the data are processed. The final analytics can be seen from the output of the 
__customer1consumer__

More information are provided inside the project report:

    assignment-3/reports/Report.md
