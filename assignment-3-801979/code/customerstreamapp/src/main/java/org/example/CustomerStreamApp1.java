package org.example;

import org.apache.flink.api.common.functions.MapFunction;
import org.apache.flink.api.common.serialization.SimpleStringSchema;
import org.apache.flink.api.java.tuple.Tuple;
import org.apache.flink.api.java.tuple.Tuple17;
import org.apache.flink.api.java.tuple.Tuple4;
import org.apache.flink.streaming.api.CheckpointingMode;
import org.apache.flink.streaming.api.TimeCharacteristic;
import org.apache.flink.streaming.api.datastream.DataStream;
import org.apache.flink.streaming.api.datastream.SingleOutputStreamOperator;
import org.apache.flink.streaming.api.environment.StreamExecutionEnvironment;
import org.apache.flink.streaming.api.functions.windowing.WindowFunction;
import org.apache.flink.streaming.api.windowing.time.Time;
import org.apache.flink.streaming.api.windowing.windows.TimeWindow;
import org.apache.flink.streaming.connectors.rabbitmq.RMQSink;
import org.apache.flink.streaming.connectors.rabbitmq.RMQSource;
import org.apache.flink.streaming.connectors.rabbitmq.common.RMQConnectionConfig;
import org.apache.flink.util.Collector;
import scala.Int;
import java.util.regex.Pattern;

import java.util.Iterator;

public class CustomerStreamApp1 {

    public static String getDate(String s) {
        String[] companies = s.split(" ");
        return companies[0];
    }

    public static void main(String[] args) throws Exception {

        //using flink ParameterTool to parse input parameters
        // final String input_rabbitMQ;
        final String input_rabbitMQ = "amqp://guest:guest@localhost:5672/";
        final String inputQueue = "customer1queue";
        final String outputQueue = "result1";
        // the following is for setting up the execution getExecutionEnvironment
        final StreamExecutionEnvironment env = StreamExecutionEnvironment.getExecutionEnvironment();
        SimpleStringSchema inputSchema =new SimpleStringSchema();

        //checkpoint can be used for  different levels of message guarantees
        // select one of the following modes
        //final CheckpointingMode checkpointingMode = CheckpointingMode.EXACTLY_ONCE ;
        final CheckpointingMode checkpointingMode = CheckpointingMode.AT_LEAST_ONCE;
        //env.enableCheckpointing(1000*60, checkpointingMode);
        // define the event time
        //env.setStreamTimeCharacteristic(TimeCharacteristic.ProcessingTime);
        //env.setStreamTimeCharacteristic(TimeCharacteristic.EventTime);
        //if using EventTime, then we need to assignTimestampsAndWatermarks
        //now start with the source of data

        final RMQConnectionConfig connectionConfig = new 	RMQConnectionConfig.Builder()
                .setHost("localhost")
                .setPort(5672)
                .setUserName("guest")
                .setPassword("guest")
                .setVirtualHost("/")
                //.setUri(input_rabbitMQ)
                .build();

        RMQSource<String> datasource= new RMQSource(
                connectionConfig,            // config for the RabbitMQ connection
                inputQueue,                 // name of the RabbitMQ queue to consume
                false,       // no correlation between event
                inputSchema);

        final DataStream<String> datastream = env
                .addSource(datasource)   // deserialization schema for input
                .setParallelism(1);

        // Input description
        //     0            1                       2                  3             4            5             6               7               8             9            10
        // VendorID,tpep_pickup_datetime,tpep_dropoff_datetime,passenger_count,trip_distance,RatecodeID,store_and_fwd_flag,PULocationID,DOLocationID,payment_type,fare_amount,
        //   11     12      13         14                   15             16
        // extra,mta_tax,tip_amount,tolls_amount,improvement_surcharge,total_amount

        // OUTPUT
        //   7 --> 0            1          2     3
        // PULocationID, number_of_taxi, date, hour
        //

        env.setStreamTimeCharacteristic(TimeCharacteristic.ProcessingTime);

        SingleOutputStreamOperator<String> mapStr = datastream.map(new MapFunction<String, Tuple4<Integer, Integer, String, String>>() {
            @Override
            public Tuple4<Integer, Integer, String, String> map(String s) throws Exception {

                String[] fieldArray = s.split(",");
                Tuple4<Integer, Integer, String, String> out = new
                        Tuple4<>(Integer.parseInt(fieldArray[7]),1 , fieldArray[2], fieldArray[2]);
                return out;
            }
            // the time window in the proper case should be set at 1 hours (Time.hours(1)). In order to test the system the system the time has been reduced
        }).keyBy(0).timeWindow(Time.seconds(1)).apply(new WindowFunction<Tuple4<Integer, Integer, String, String>, String, Tuple, TimeWindow>() {
            @Override
            public void apply(Tuple tuple, TimeWindow timeWindow, Iterable<Tuple4<Integer, Integer, String, String>> iterable, Collector<String> collector) throws Exception {

                Iterator<Tuple4<Integer, Integer, String, String>> iterator = iterable.iterator();
                Tuple4<Integer,Integer, String, String> event1 = iterator.next();

                int PULocationID = event1.f0;
                int number_of_taxi = 1;
                String date = getDate(event1.f2);
                long hour = timeWindow.getEnd();

                while (iterator.hasNext()) {
                    number_of_taxi++;
                    iterator.next();
                }

                collector.collect("{\"PULocationID\":"+ Integer.toString(PULocationID) +
                        ", \"number_of_taxi\":" + Integer.toString(number_of_taxi) +
                        ", \"date\":" + date +
                        ", \"hour\":" + Long.toString(hour) +
                        "}");
            }
        });

        //send the alerts to another channel
        RMQSink<String> sink =new RMQSink<String>(
                connectionConfig,
                outputQueue,
                new SimpleStringSchema());

        mapStr.addSink(sink);

        env.execute("CustomerStreamAPP1");

    }
}
