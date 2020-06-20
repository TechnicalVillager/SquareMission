#!/bin/sh
echo "This script will execute square mission in FlytSim simulator."
read -p "Please Enter Altitude   : " alt
read -p "Please Enter Side Length: " side
echo "Altitude is $alt and Side Length is $side"
python first_flight.py $alt $side