import os
import json
from azure.data.tables import TableServiceClient
from dotenv import load_dotenv

load_dotenv()
# azure-data-tables==12.6.0
def set_trend_data(treding_json):
    connection_string = os.environ["TABLE_CONNECTION"]  # put in settings
    table_name = "trending"

    # Connect to the service and table
    service = TableServiceClient.from_connection_string(conn_str=connection_string)
    table_client = service.get_table_client(table_name=table_name)

    # Upsert (add/update) data
    trend_data = {
        "PartitionKey": "trends",
        "RowKey": "curr_trend",
        "data": json.dumps(treding_json)
    }
    table_client.upsert_entity(trend_data)

def get_trend_data():
    connection_string = os.environ["TABLE_CONNECTION"]  # put in settings
    table_name = "trending"

    # Connect to the service and table
    service = TableServiceClient.from_connection_string(conn_str=connection_string)
    table_client = service.get_table_client(table_name=table_name)

    # Retrieve data
    entity = table_client.get_entity(partition_key="trends", row_key="curr_trend")
    trend_data = json.loads(entity["data"])
    
    return trend_data
