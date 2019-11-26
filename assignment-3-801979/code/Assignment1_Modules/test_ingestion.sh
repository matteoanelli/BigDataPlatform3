#!/bin/bash
for i in {1..10}; do
    time (python ingestSource.py "/home/matteo/Downloads/Indoor_Location_Detection_Dataset.csv") &
done

wait
