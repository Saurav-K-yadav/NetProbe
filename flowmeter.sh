#!/bin/bash

# Activate virtual environment
#bash newscript.sh &



source venv3/bin/activate
echo "STARTING FLOWMETER"


cicflowmeter -i enp0s3 -c test.csv 

