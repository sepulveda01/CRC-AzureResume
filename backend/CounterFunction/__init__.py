import os
import json
import azure.functions as func
from azure.cosmos import CosmosClient, exceptions
from azure.identity import DefaultAzureCredential

COSMOS_ENDPOINT = os.environ["COSMOS_ENDPOINT"]
COSMOS_DATABASE = os.environ.get("COSMOS_DATABASE", "AzureResume")
COSMOS_CONTAINER = os.environ.get("COSMOS_CONTAINER", "Counter")
COUNTER_ID = os.environ.get("COUNTER_ID", "my_counter")


def main(req: func.HttpRequest) -> func.HttpResponse:
    credential = DefaultAzureCredential()
    client = CosmosClient(COSMOS_ENDPOINT, credential=credential)
    container = client.get_database_client(COSMOS_DATABASE).get_container_client(COSMOS_CONTAINER)

    try:
        item = container.read_item(item=COUNTER_ID, partition_key=COUNTER_ID)
        item["count"] = int(item.get("count", 0)) + 1
        container.replace_item(item=COUNTER_ID, body=item)

    except exceptions.CosmosResourceNotFoundError:
        item = {"id": COUNTER_ID, "count": 1}
        container.create_item(body=item)

    return func.HttpResponse(
        json.dumps({"count": item["count"]}),
        mimetype="application/json",
        status_code=200,
    )