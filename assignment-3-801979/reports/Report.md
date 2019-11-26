# Assignment 2 Report - working on data ingestion features - 801979
As first part of the report, an overview of the designed and implemented structure will be explained. Moreover, the connections with the first assignment will be introduced in order to continue with the course story. 
The focus of this assignment is on the data ingestion part of the structure. In general it is divided in two main flows, the batch-ingestion part and the real-time ingestion. Although, this difference has been already highlighted in the previous assignment, some additional features were required in this second one. The main different constraint is that the platform in this assignment have to deal with multi-tenancy as a result the design required a different configuration. Each customer has its own data but it has been assumed that all of them use the same database/storage model. The data sink has been implemented using mongoDB Atlas, thus, the data model selected is document-based. In addition, the customer is the one that will design the data structure.

Following the structure implemented in the first assignment: 

![](Implementation.png)

To sum up, the user can import the sources using the source ingestion script that is directly connected with mongoDB. MongoDB Atlas provides a cloud solution where a cluster of 3 nodes have been created so that all the data are stored and replicated. Afterword, the user can interact with the Flask end point and make POST/GET requests. In the case of POST requests, they are forwarded to the message broker(RabbitMQ). In the case of GET requests they are forwarded directly to the mongoDB data storage. To highlight, RabbitMQ has been implemented as a Service using the CloudAMQP webservice. This choice was made to speed up the implementation time.

#### New implementation

Starting from the previous implementation the new architecture has been designed. Some of the components have been reused and adapted to the new constraints. The same data sink have been used for his implementation practicality, mongoDB Atlas provide a consistent and easy to use solution. The multi-tenancy require different components and the design has to be adapted as well. Following the new design in brief: 

![](BasicImplementation.png)

The above picture shows the general design of the architecture, it is mainly divided in two flow as mentioned before. The batch ingestion allow multiple users to send data as CSV files to the platform. After that, a component (fetchData) automatically detect which file should be ingested based on some predefined constraints. Once the files are validated, they will be pushed inside the staging data, in our case a local directory where they wait the batchManager to forward them to the correct customer batch ingestion app. Finally, the data will be pushed to the data sink. Regarding the near realtime ingestion flow users can interact with the platform throughout API. They can send POST request to the server which will forward the data to the message broker. After that a streaming manager will activate the needed customer stream ingestion application in charge to push the messages to the data sink. 

During the project some technologies have been explored and analysed to implement the different components. Given the inexperience as well as the number of potential different solutions, this process took a lot of time of the overall time spent to do the assignment. In the following picture the final implemented architecture is shown:

![](NewArchitecture.png)

Regarding the batch ingestion, each custumer push the data inside a specific client directory. The fetch data component has been implemented with Apache Nifi. The basic idea is to create a workflow where the data can be validated and sent it to a common directory, the staging data directory. Along with Nifi, some other possible technologies have been analysed such as Apache Airflows. At the end, Nifi appear as the best solution to implement for some reasons: in a fast way a reproducible workflaw can be generated, it provide a suit of features such as input filters that were really useful in the assignment scenario. Eventually, it provid also some feature to do microbatching solutions. Nifi will be on the client side, that has to easily import our pre-defined workflow and set the input directory. Nifi will take care of the rest, more details later in the report. To simulate easely and quikly this part, 2 customers have been simulated as well as the output staging data directory is a local folder inside the project directory. The staging directory has been organized such that for each customer exist a sub-folder with all the related input files inside. Once the files are inside the staging directory, the manager will forward them to the relative client application. The manager implementation consist as a python script that each 30 second fetch the staging directory and forward the input files to the customers ingestion applications. The final objects of the batch ingestion pipeline before the data sink are the client application. Those are python script provided by the customers that aim to ingest the input file to the final sink. These applications are coded by the customers so that they can chose how to structure the data. The applications integrity and consistency is checked in the beginning by an expert. All the files tracking and forwarding as well as the staging directory structure is based on an client ID previously assigned so that knowing the customer id the respective folder can be identified as well as the right application can be triggered.

Regarding the near realtime ingestion flow, the clients send messages to a Flusk endpoint. In this way the input format has been limited. More information later in the report. The message structure guarantee the platform to know the customer id in the beginning, this is used to create a different queue for each customer inside the message broker. In this way all the different messages can be listened by the right customer application, as a result, the will be pushed in the right databases. Once the messages are pushed inside the broker the manager will trigger the different customer stream ingestion applications that are consumer coded by each customer. They have to listen the messages on each customer queue and push the message inside the final data sink. The broker used is the same as in the previous assignment, the rabbitMQ solution cloudAMQP.

To summarize the platform overview, the different client are managed inside the platform throughout the unique customer ID. They have some constraint to respect on the type of input file and format of input data. On the other hand, each customer can have his own database and can menage the structure of the database without restriction. 

#### Platform and client tasks
To point out in the project are the task that the platform have to perform and the one that the customers have to do. The customer have locally to install Nifi in order to import our data workflow. Moreover, the ingestion applications have to be implemented by the client. In this way, the client can have control on the data pushed as well as the platform does not need to have access on the client data. In addition, the customer has to respect the constraint imposed by the platform about the message structure.  The platform is in charge to all the scalability of the system and it has to provide the aspected level of service to all the different customers

# Part 1 - Ingestion with batch
#### 1. 2. Input constraint and fetchdata component
The constraint on the input file have been done directly in Nefi, is role is to filter the file and forward them to the staging directory. The input constraint are:
- The input file should be a CSV file
- The maximum size allowed is 2 GB
Thinking in a future scenario, in this way since we pass our workflow to each customer, the constraint can be modified and adapted based on different profiles. 

The main structure of or **mysimbdp-fetchdata** is the following:

![](Nifi.png)

As we can see form the above picture, the structure is a directed graph that define some action to do. The first action is the getFile. The client has to specify the input directory, the process getFill is a listener that as soon as a file will be added inside the client input directory it will be pushed on the Nifi workflow. Once the get have been concluded successfully the input file will be removed from the directory. 
The configuration properties are the following:

![](inputConf.png)

As we can see a filter on the file format has been done as well as a limit on the maximum file size has been set. As a result, the getFile process will ingest only the files that respect both the requirement. Changing those properties different custom configuration can be implemented. 

The second processor inside the workflow is the so called SplitRecord. Set a define dimension this process will split, if bigger, the input file in sub file with the set size. After that, it will forward the output files to the next process. Explained this process in the micro-batching section later inside the report.

The third processor is the so called updateAttribute that is used to add the timestamp to the new files generated name. Without it only the last file will be found inside the output directory. 
The configuration is the following:

![](update.png) 

The last active process is the putFile, it receive the file from the queue and it will push the file inside the pre-defined output directory. This output directory is common between all the clients. For simplicity of implementation this output is a local directory inside the assignment repository. This can be extended in some different ways, one of those could be targeting a common directory in a cloud such as google cloud. Nifi provide some complementary put method to extend this usage.

Finally, some logging processes have been included in the workflow to catch different potential failure. 

Two different client have been implemented inside the test environment.

Following an example of the staging data directory:

```
StagingDirectory
│
└───tenant1
│     └─── file011.csv
│     └─── file012.csv
│   
└───tenant2
│     └─── file011.csv
│     └─── file012.csv
.
.
```
Where tenant1 and tenant2 aare the 2 client ID.

#### 3. Batch ingestion manager and client batch ingest applications
The batch ingestion manager is a python script that each 30 second will fetch the content of the staging directory and it will forward the files to the respective ingest application. 
In order to know the different ID and use the different application a configuration file has been implemented with all the information needed. 
```
{
  "tenants": [{
    "tenant_id": "tenant1",
    "password": "XXXXXXX",
    "MONGO_URL": "mongodb+srv://tennant1:XXXXXXX@mysimbdp-coredms-novzr.mongodb.net/test?retryWrites=true&w=majority",
  },
    {
    "tenant_id": "tenant2",
      "password": "YYYYYYYYYY",
    "MONGO_URL": "mongodb+srv://tennant1:YYYYYYYYY@mysimbdp-coredms-novzr.mongodb.net/test?retryWrites=true&w=majority"
  }
  ]
}

```
The manager call the different customer application. The clients has to know that both the input file as well as the connection url needed will be passed as argument like that:
```   
python clientbatchingest_tenantX.py <input_file_path> <mongo_url_connection>
```                                                                                

Knowing this the client should be able to code the ingest application without any problem. 
To test the implementation client application have been coded.




#### 4. Test program

#### 5. Logging features




# Part 2 - Near-realtime ingestsion 
#### 1. Message structure
A simple message structure that all the customer have to use has been fixed. The customer interact with the platform through a Flask API where all the check of the consistency of the message are made. The structure is the following:
```

{
	"tenant_id": "tenant1",
	"data" : { no limit on data }   
}
    
```        
The imposed structure consist of a json file. It require the **tenant_id** that it will be used to create the queue and forward the messages and a dictionary as data with out any limit of the fields.

#### 2. Data broker
As data broker rabbitMQ has been used to queue the customer messages. In the implementation for each customer a queue with the routing key set as **tenant_id** will be generated where the consumers can consume the messages. Following an example of the queue in action with the two test clients:

![](queue.png)

#### 2. Batch ingestion manager and client batch ingest applications

#### 3. Test Data

#### 4. Design Report Format
The report format can be a json file with inside the tenant_id and all the metrics calculated. This file is generated by the application. It will be send each X sec to a queue of the broker with a particular key_rote. The report could be like:
```
{
  "tenant_id": "tenant1",
  "average_ingestion_time": "XXXXXXX",
  "data_size": "ZZZZZZZ",
  "number_of_messages_ingested_per_sec": "YYYYYYYY"
   .
   .
   .
}

```
An additional consumer have to be created that listening to the report messages, based on the metrics will launch new instances or will kill some instances to balance the number of active application. Since inside the report there is the tenant_id the consumer can know which client application has to be balanced.

#### 5. Implementation Report

# Part 3 - Integration and Extension   
#### 1. Integrated architecture
A possible integrated architecture solution is the so called kappa solution where the batch layer have been removed. To replace batch processing, data is simply fed through the streaming system quickly using the real time process. In our case all the batching process should be removed and the customer should pre-process the input file so that it can be sent it as messages to the API. 

#### 2. Solution to files too big for our implementation
In the assigment implementation, the filter on the file dimension is done with Nifi on the client side. As a result, it is difficult to think of a quickly solution. One possible solution to the problem is that the client should split the input file in sub-files that respect input constraint. 
#### 3. Platform provided should not see the code
As a platform provided we should not see the code of the customer since inside there might be some sensitive information and the platform should guarantee the customer privacy. 
#### 4. Quality of data
In order to maintain a certain level of data quality, some constraint can be set. First of all, some additional check on the input data can be done. Moreover, some limit on the data structure can be fixed as well. As a result, the client have to check the quality of the data before send them to the platform. In addition, as platform provided we can do some additional quality check before the final ingestion to the data sink.
#### 5. Multiple client apps
A possible solution of the multiple client app situation is: for the batch process that inside the staging directory an additional level of sub-directory can be generated so that from that we can map with the application name. The directory could like this:
```
StagingDirectory
│
└───tenant1
|    └─── tenant1app1
│      └─── file011.csv
│      └─── file012.csv
|    └─── tenant1app2
│      └─── file021.csv
│      └─── file022.csv
│   
└───tenant2
    └─── tenant2app1
│     └─── file011.csv
│     └─── file012.csv
.
.
```
Regarding the streaming process the concept of topic can be used so that inside the customer queue we can found messages from different topics.


# Bonus Points
#### Implementation of dynamic management


#### Automatic switch to micro-batching

As we mentioned in the first part of the report, Nifi provides some solutions for micro-batching. Specifically, it has been done using the splitRecord processor. The process will automatically split the input data in micro-batches if the file is bigger than a defined threshold. The defined value during the tests is 1000 record per split.

![](split.png)



# to do 
- second database
- streaming manager 
- rabbit link in arguments