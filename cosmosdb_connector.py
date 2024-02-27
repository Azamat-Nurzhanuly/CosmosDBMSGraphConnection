import asyncio
import configparser

from cosmosdb_graph import CosmosGraph


async def main():
    print('Python Graph Connector\n')

    # Load settings
    config = configparser.ConfigParser()
    config.read(['config.cfg'])
    azure_settings = config['azure']

    graph: CosmosGraph = CosmosGraph(azure_settings)

    await graph.create_connection()
    await graph.create_schema()

    await graph.create_items(objects=get_data())


def get_data():
    from azure.cosmos import CosmosClient, exceptions

    # Initialize the Cosmos client
    cosmos_client = CosmosClient(url="<COSMOSDB_URL>", credential="<CREDENTIALS>")
    database = cosmos_client.get_database_client("DB")
    container = database.get_container_client("CONTAINER")

    # Query items (adjust query as needed)
    items = list(container.query_items(
        query="SELECT * FROM c",
        enable_cross_partition_query=True
    ))

    return items

# Run main
asyncio.run(main())
