import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Temporary stub to prove routing + deployment works
    return func.HttpResponse(
        json.dumps({"count": 0}),
        mimetype="application/json",
        status_code=200,
    )
