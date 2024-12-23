from flask import Flask, Response
import requests
from prometheus_client import CollectorRegistry, Gauge, generate_latest
from dotenv import load_dotenv
import os
from pprint import pprint

# Load environment variables from .env file
load_dotenv()

# Flask application
app = Flask(__name__)

# Prometheus registry
registry = CollectorRegistry()

# Prometheus metrics
total_subscribers_gauge = Gauge('sendy_total_subscribers', 'Total subscribers count', ['list_id', 'list_name'], registry=registry)
#active_subscribers_gauge = Gauge('sendy_active_subscribers', 'Active subscribers count', ['list_id', 'list_name'], registry=registry)

# Sendy API details from environment variables
SENDY_API_URL = os.getenv("SENDY_API_URL")
SENDY_API_KEY = os.getenv("SENDY_API_KEY")
SENDY_BRAND_ID = os.getenv("SENDY_BRAND_ID")

@app.route("/metrics")
def metrics():
    """Endpoint to expose Prometheus metrics."""
    try:
        # Fetch all lists
        response = requests.post(SENDY_API_URL+"/lists/get-lists.php", data={
            'api_key': SENDY_API_KEY,
            'boolean': 'true',
            'brand_id': SENDY_BRAND_ID,
        })

        if response.status_code == 200:
            #pprint(response.text)
            lists = response.json()
            #pprint(lists)

            for mailing_list in lists.keys():
                _mailing_list = lists[mailing_list]
                #pprint(_mailing_list)
 
                list_id = _mailing_list.get('id')
                list_name = _mailing_list.get('name', 'unknown')
                try:
                    # Fetch data for each list
                    list_response = requests.post(SENDY_API_URL+ '/' + "/subscribers/active-subscriber-count.php", data={
                        'api_key': SENDY_API_KEY,
                        'list_id': list_id,
                    })

                    if list_response.status_code == 200:
                        data = list_response.json()
                        #pprint(data)

                        total_subscribers = data
                        #active_subscribers = int(data.get('active_subscribers', 0))

                        total_subscribers_gauge.labels(list_id=list_id, list_name=list_name).set(total_subscribers)
                        #active_subscribers_gauge.labels(list_id=list_id, list_name=list_name).set(active_subscribers)
                    else:
                        print(f"Error fetching data for list {list_id} ({list_name}): {list_response.text}")
                except Exception as e:
                    print(f"Exception occurred for list {list_id} ({list_name}): {e}")
        else:
            print(f"Error fetching lists: {response.text}")

    except Exception as e:
        print(f"Exception occurred while fetching lists: {e}")

    return Response(generate_latest(registry), mimetype='text/plain')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.getenv("EXPORTER_PORT"))
