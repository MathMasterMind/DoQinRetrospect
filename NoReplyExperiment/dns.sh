#!/bin/bash

# Read IP addresses from addresses.txt
while IFS=, read -r name ip; do
    # Strip leading/trailing spaces from IP and name
    ip=$(echo "$ip" | xargs)
    name=$(echo "$name" | xargs)

    if [[ -z "$ip" || -z "$name" ]]; then
        continue
    fi

    # Output files for packet_measure.py
    output_file="./dns_logs/results_$ip.csv"

    # Run packet_measure.py for the current IP and store output in CSV
    sudo python measure.py "$ip" "$output_file" &

    # Run DNS.py in the background for the current IP
    sudo python DNS.py "$ip" &

    sleep 30s
done < ../addresses.txt

# Wait for all background processes to complete
wait
