# ECE6612 Project

This repository contains tools and experiments for exploring QUIC and DNS over QUIC (DoQ) protocols. It leverages the `aioquic` library, a Python implementation of QUIC and HTTP/3.

## Repository Structure

```
.
├── runner.sh                # Script to set up and run experiments
├── requirements.txt         # Python dependencies
├── packet_measure.py        # Script for packet measurement
├── aioquic/                 # Submodule for aioquic library
├── RetryExperiment/         # Scripts for retry-related experiments
├── ServerAquisition/        # Tools for server acquisition and analysis
├── UnpaddedExperiment/      # Scripts and patches for unpadded QUIC experiments
└── ...
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- `git` for managing submodules

### Setup

1. Clone the repository:
   ```bash
   git clone --recursive https://github.com/MathMasterMind/DoQinRetrospect.git
   ```

2. Run the setup script:
   ```bash
   ./runner.sh
   ```

   This script:
   - Initializes and updates the aioquic submodule.
   - Sets up a Python virtual environment.
   - Installs required dependencies.
   - Applies the `nopad.patch` for the unpadded QUIC experiment.
   - Runs the `unpadded_connection.py` script.

### Experiments

#### Unpadded QUIC Experiment

The UnpaddedExperiment directory contains:
- `nopad.patch`: A patch to modify the aioquic library for unpadded QUIC connections.
- `unpadded_connection.py`: A script to test unpadded QUIC connections.

To run this experiment, execute:
```bash
./runner.sh
```

#### Retry Experiments

The RetryExperiment directory includes:
- `DoT_Client_Hello.py`: Simulates a DNS-over-TLS client hello.
- `DoT_No_Reply.py`: Sends a DoT client SYN Packet.
- `DoQ_Initial.py`: Sends a DoQ client Initial Packet.

Use Wireshark to monitor traffic

#### Server Acquisition

The ServerAquisition directory contains tools for analyzing QUIC servers:
- `ip_to_globe.py`: Maps IP addresses to geographical locations.
- `quic_resolvers_src1.py` and `quic_resolvers_src2.py`: Scripts for resolving QUIC servers.

