# Secure File Integrity Checker

A professional-grade tool to monitor and verify the integrity of files using cryptographic hashing.

## Features
- **Baseline Creation**: Generate a secure snapshot of your files.
- **Integrity Verification**: Compare current file states against the baseline to detect unauthorized changes.
- **Multiple Hash Algorithms**: Support for SHA-256, SHA-512, and BLAKE3.
- **Detailed Reporting**: Identify new, modified, and deleted files.
- **Configurable**: Use YAML files to exclude paths or change algorithms.

## Installation
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install .
```

## Usage
### Create Baseline
```bash
secure-integrity baseline /path/to/monitor
```

### Verify Integrity
```bash
secure-integrity verify /path/to/monitor
```

## How it Works
The tool computes hashes for every file in the target directory and stores them in a local SQLite database. During verification, it re-computes hashes and compares them with the stored values.
