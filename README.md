# Automotive CAN Fuzzer

## Overview

Automotive CAN Fuzzer is a Python-based automotive cybersecurity testing tool designed to analyze CAN (Controller Area Network) communication and simulate potential security vulnerabilities.

The project focuses on fuzz testing techniques by generating modified CAN messages, testing abnormal communication scenarios, and creating security reports.

## Features

- CAN message fuzzing
- CAN ID mutation
- Payload data mutation
- CAN Flooding simulation
- Invalid payload testing
- Replay attack simulation
- Automated fuzzing scenarios
- Security event logging
- JSON, CSV and HTML report generation

## Security Test Scenarios

The tool supports different automotive CAN security test cases:

- **CAN ID Flooding**
  - Simulates excessive CAN message traffic.

- **Invalid Payload Injection**
  - Tests ECU behavior against malformed CAN data.

- **Replay Testing**
  - Replays previous CAN messages to analyze system responses.

- **Denial of Service (DoS) Simulation**
  - Tests communication robustness against abnormal traffic.

## Technologies

- Python 3
- CAN Communication
- Automotive Cyber Security
- Fuzz Testing
- Embedded System Security

## Generated Reports

The tool automatically creates security reports:

- JSON Report
- CSV Report
- HTML Report

Reports are stored in the `reports` directory.

## Future Improvements

- Real CAN hardware integration
- SocketCAN support
- ISO-TP fuzzing
- UDS security testing integration
- Advanced ECU response analysis

## Author



Automotive Cyber Security Research Project
