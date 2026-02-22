import os
import json
import azure.functions as func
from azure.cosmos import CosmosClient


COSMOS_ENDPOINT = os.environ["COSMOS_ENDPOINT"]
COSMOS_KEY = os.environ["COSMOS_KEY"]
COSMOS_DATABASE = os.environ.get("COSMOS_DATABASE", "AzureResume")
COSMOS_CONTAINER = os.environ.get("COSMOS_CONTAINER", "Counter")

COUNTER_ID = os.environ.get("COUNTER_ID", "my_counter")


def main(req: func.HttpRequest) -> func.HttpResponse:
    client = CosmosClient(COSMOS_ENDPOINT, credential=COSMOS_KEY)
    container = client.get_database_client(COSMOS_DATABASE).get_container_client(COSMOS_CONTAINER)

    # Read the counter document
    item = container.read_item(item=COUNTER_ID, partition_key=COUNTER_ID)

    # Increment
    current = int(item.get("count", 0))
    new_count = current + 1
    item["count"] = new_count

    # Write back
    container.replace_item(item=COUNTER_ID, body=item)

    return func.HttpResponse(
        json.dumps({"count": new_count}),
        mimetype="application/json",
        status_code=200,
    )
