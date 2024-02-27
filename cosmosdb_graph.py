from configparser import SectionProxy
from azure.identity import ClientSecretCredential
from msgraph import GraphServiceClient
from msgraph.generated.models.external_connectors.external_connection import ExternalConnection
from msgraph.generated.models.external_connectors.schema import Schema
from msgraph.generated.models.external_connectors.property_ import Property_
from msgraph.generated.models.external_connectors.property_type import PropertyType
from msgraph.generated.models.external_connectors.access_type import AccessType
from msgraph.generated.models.external_connectors.acl import Acl
from msgraph.generated.models.external_connectors.acl_type import AclType
from msgraph.generated.models.external_connectors.external_item import ExternalItem
from msgraph.generated.models.external_connectors.properties import Properties


class CosmosGraph:
    settings: SectionProxy
    cred: ClientSecretCredential
    user_client: GraphServiceClient
    connection_id: str
    connection_name: str
    connection_description: str

    def __init__(self, config: SectionProxy):
        self.settings = config
        client_id = self.settings['clientId']
        tenant_id = self.settings['tenantId']
        client_secret = self.settings['client_secret']

        self.connection_id = "cosmosdbconnector"
        self.connection_name = "CosmosDB Connector"
        self.connection_description = "Custom CosmosDB Connector"

        self.cred = ClientSecretCredential(client_id=client_id, tenant_id=tenant_id, client_secret=client_secret, scope="https://graph.microsoft.com/.default")
        self.user_client = GraphServiceClient(self.cred)

    async def create_connection(self):
        # create prompt for user to enter connection details
        new_connection = ExternalConnection(
            id=self.connection_id,
            name=self.connection_name,
            description=self.connection_description,
        )

        print("Creating connection...")
        connection = await self.user_client.external.connections.post(body=new_connection)
        print("Connection created successfully! Connection name:", connection.name)

    async def create_schema(self):
        schema = Schema(
            base_type="microsoft.graph.externalItem",
            properties=[
                Property_(
                    name="id",
                    type=PropertyType.String,
                    is_searchable=True,
                    is_retrievable=True,
                ),
                Property_(
                    name="Code",
                    type=PropertyType.String,
                    is_retrievable=True,
                ),
                Property_(
                    name="Description",
                    type=PropertyType.String,
                    is_searchable=True,
                    is_retrievable=True,
                ),
            ]
        )
        print("Creating schema...")
        await self.user_client.external.connections.by_external_connection_id(self.connection_id).schema.patch(schema)
        print("Schema created successfully!")

    async def create_items(self, objects: list):
        for obj in objects:
            print("Creating item for obj: ", obj["Code"])
            request_body = ExternalItem(
                id=obj["Code"],
                acl=[
                    Acl(
                        type=AclType.Group,
                        value="<ACL_ID>",
                        access_type=AccessType.Grant
                    )
                ],
                properties=Properties(
                    additional_data={
                        "Code": obj["Code"],
                        "Description": obj["Description"],
                        "id": obj["id"]
                    }
                )
            )

            await self.user_client.external.connections.by_external_connection_id(
                self.connection_id).items.by_external_item_id(request_body.id).put(request_body)
            print("Item created successfully!")
