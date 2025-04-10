sudo iptables -I OUTPUT -p udp --dport 853 -j NFQUEUE --queue-num 1

# run test

sudo iptables -D OUTPUT -p udp --dport 853 -j NFQUEUE --queue-num 1

sudo iptables -L -v -n
