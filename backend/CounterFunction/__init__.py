import os
import json
import azure.functions as func
from azure.cosmos import CosmosClient, exceptions


COSMOS_ENDPOINT = os.environ["COSMOS_ENDPOINT"]
COSMOS_KEY = os.environ["COSMOS_KEY"]
COSMOS_DATABASE = os.environ.get("COSMOS_DATABASE", "AzureResume")
COSMOS_CONTAINER = os.environ.get("COSMOS_CONTAINER", "Counter")
COUNTER_ID = os.environ.get("COUNTER_ID", "my_counter")


def main(req: func.HttpRequest) -> func.HttpResponse:
    client = CosmosClient(COSMOS_ENDPOINT, credential=COSMOS_KEY)
    container = client.get_database_client(COSMOS_DATABASE).get_container_client(COSMOS_CONTAINER)

    try:
        # Try to read existing document
        item = container.read_item(item=COUNTER_ID, partition_key=COUNTER_ID)
        current = int(item.get("count", 0))
        item["count"] = current + 1

        container.replace_item(item=COUNTER_ID, body=item)

    except exceptions.CosmosResourceNotFoundError:
        # If it doesn't exist yet, create it
        item = {
            "id": COUNTER_ID,
            "count": 1
        }
        container.create_item(body=item)

    return func.HttpResponse(
        json.dumps({"count": item["count"]}),
        mimetype="application/json",
        status_code=200,
    )
