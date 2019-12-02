Instruction for deployment
=====================

The project have been developed in python and Java. Be sure to use version 3.6+ and Java 8+. Moreover Maven should be installed as well as 
Apache Flink 1.9.1+.

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

To point out that during the testing I had some issues with Maven and some dependencies. 
So if some issue running the Jar file occur it is possible to run it from the Flink web server at http://localhost:8081. 
Here, it always worked. (Remember to set parallelism to 1)