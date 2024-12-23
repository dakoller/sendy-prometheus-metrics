# Sendy Prometheus Metrics Exporter

## Overview
This Python script collects data from a [Sendy](https://sendy.co/) installation and exposes it as metrics in a format compatible with Prometheus. The metrics provide insights into the total and active subscriber counts for all mailing lists configured in the Sendy system.

## Features
- Dynamically fetches all mailing lists from Sendy.
- Exposes metrics for total subscriber count per list.
- Integrates with Prometheus for monitoring and alerting.

## Metrics
The following metrics are exposed:
- `sendy_total_subscribers`: Total number of subscribers for each mailing list.
  - Labels: `list_id`, `list_name`


## Prerequisites
- Python 3.7+
- [Sendy](https://sendy.co/) API credentials.
- Prometheus installed and configured.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/dakoller/sendy-prometheus-metrics.git
   cd sendy-prometheus-metrics
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with the following content:
   ```env
   SENDY_API_URL=https://your_sendy_installation/api
   SENDY_API_KEY=your_sendy_api_key
   EXPORTER_PORT=8000  # Optional, default is 8000
   ```

## Usage
1. Run the script:
   ```bash
   python run_exporter.py
   ```

2. The metrics will be exposed at `http://<host>:<METRICS_PORT>/metrics`.

## Prometheus Integration
1. Add the metrics endpoint to your Prometheus configuration:
   ```yaml
   scrape_configs:
     - job_name: 'sendy'
       static_configs:
         - targets: ['<host>:<METRICS_PORT>']
   ```

2. Reload your Prometheus configuration to apply the changes.

## Example Output
Example metrics exposed by the script:
```
# HELP sendy_total_subscribers Total subscribers count
# TYPE sendy_total_subscribers gauge
sendy_total_subscribers{list_id="1",list_name="Newsletter"} 150
sendy_total_subscribers{list_id="2",list_name="Updates"} 200

## Notes
- Ensure that the Sendy API key has the necessary permissions to access all lists.
- Use proper security measures to protect your API credentials and metrics endpoint.

## Troubleshooting
1. If the metrics are not appearing:
   - Check the `.env` file for correct values.
   - Verify that the Sendy API is reachable.

2. For connection issues:
   - Ensure the host running the script is accessible by Prometheus.
   - Check for firewall or network restrictions.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

