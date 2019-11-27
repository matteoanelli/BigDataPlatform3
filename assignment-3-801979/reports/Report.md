# Assignment 3 Report - Understanding Big Data Processing - 801979


## Part 1 - Design for streaming analytics
1. The selected dataset for this project is one the [NYC taxi Dataset](https://data.cityofnewyork.us/Transportation/2018-Yellow-Taxi-Trip-Data/t29m-gskq), it contains the yellow taxi trip records. The records are provided by two TPEP provider and they contain information about the time and the trip of the location as well as some additional information such as the tips amounts and the number of passenger. The main relevant fields for the analysis are: 
* The __tpep_pickup_datetime__, the date and time when the meter was engaged. 
* The __tpep_dropoff_datetime__, the dateand time when the mettetr was disengaged.
* The __PULocationID__, TLC Taxi Zone in which the taximeter was engaged.
* The __DOLocationID__  TLC Taxi Zone in which the taximeter was disengaged.

Some analytics has been defined for the customer:

i) A streaming analytics that, in a defined period of time, counts the number of taxi engaged in a specific taxi zone. Thus, the taxi provider know where there is the more request of taxi in a specific time, or a threshold can be set and when the number of taxi is grater than this threshold the taxi company can be warned, as a result, it can organize its taxi fleet accordingly. Another analytics can be done by counting the number of Group rides (Information that can be found inside __RateCodeID__) so that, in a specific amount of time. If the number of group trip is grater than usual the vendors can locate their "XL" Taxis.

ii) A batch analytics that, given the output from the streaming analytics can provide daily, weekly or monthly statistics to the vendors. For example, the streaming analytics is agglomerating based on specific taxi area the number of taxi that have been engaged per hour. Hence, the most frequented area per day can be calculated.

2\. The customer will send the data to the message broker which become the data stream sources. The taxi record are sent simulating a stream as in a real case scenario:

i) The analytics is handled in keyed data streams, the records stream is keyed by __PULocationID__ divided the data in different streams so that a time window can be set.
## Part 2 - Implementation of streaming analytics

## Part 3 - Connection


