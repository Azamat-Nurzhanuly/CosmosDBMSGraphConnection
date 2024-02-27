# CosmosDB MS Graph Connection
[Microsoft Graph SDK for Python](https://github.com/microsoftgraph/msgraph-sdk-python).

## 1. Installation

```py
pip install -r requirements.txt
```

## 2. Getting started with Microsoft Graph

### 2.1 Register your application

Register your application by following the steps at [Register your app with the Microsoft Identity Platform](https://docs.microsoft.com/graph/auth-register-app-v2).

### 2.2 Select and create an authentication provider

To start writing code and making requests to the Microsoft Graph service, you need to set up an authentication provider. This object will authenticate your requests to Microsoft Graph. For authentication, the Microsoft Graph Python SDK supports both sync and async credential classes from Azure Identity. Which library to choose depends on the type of application you are building.

The easiest way to filter this decision is by looking at the permissions set you'd use. Microsoft Graph supports 2 different types of permissions: delegated and application permissions:
- Application permissions are used when you don’t need a user to login to your app, but the app will perform tasks on its own and run in the background. 
- Delegated permissions, also called scopes, are used when your app requires a user to login and interact with data related to this user in a session.

The following table lists common libraries by permissions set. 
| MSAL library | Permissions set | Common use case |
|---|---|---|
| [ClientSecretCredential](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.aio.clientsecretcredential?view=azure-python&preserve-view=true) | Application permissions | Daemon apps or applications running in the background without a signed-in user. |
| [DeviceCodeCredential](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.devicecodecredential?view=azure-python) | Delegated permissions | Enviroments where authentication is triggered in one machine and completed in another e.g in a cloud server. |
| [InteractiveBrowserCredentials](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.interactivebrowsercredential?view=azure-python) | Delegated permissions | Environments where a browser is available and the user wants to key in their username/password. |
| [AuthorizationCodeCredentials](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.authorizationcodecredential?view=azure-python) | Delegated permissions | Usually for custom customer applications where the frontend calls the backend and waits for the authorization code at a particular url. |

You can also use [EnvironmentCredential](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.environmentcredential?view=azure-python), [DefaultAzureCredential](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.defaultazurecredential?view=azure-python), [OnBehalfOfCredential](https://learn.microsoft.com/en-us/python/api/azure-identity/azure.identity.onbehalfofcredential?view=azure-python), or any other [Azure Identity library](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python#credential-classes).

Once you've picked an authentication library, we can initiate the authentication provider in your app. The following example uses ClientSecretCredential with application permissions.
```python
import asyncio

from azure.identity.aio import ClientSecretCredential

credential = ClientSecretCredential("tenantID",
                                    "clientID",
                                    "clientSecret")
scopes = ['https://graph.microsoft.com/.default']
```

The following example uses DeviceCodeCredentials with delegated permissions.
```python
import asyncio

from azure.identity import DeviceCodeCredential

credential = DeviceCodeCredential("client_id",
                                  "tenant_id")
graph_scopes = ['User.Read', 'Calendars.ReadWrite.Shared']
```

### 2.3 Initialize a GraphServiceClient object

You must create **GraphServiceClient** object to make requests against the service. To create a new instance of this class, you need to provide credentials and scopes, which can authenticate requests to Microsoft Graph.

```py
# Example using async credentials and application access.
from azure.identity.aio import ClientSecretCredential
from msgraph import GraphServiceClient

credentials = ClientSecretCredential(
    'TENANT_ID',
    'CLIENT_ID',
    'CLIENT_SECRET',
)
scopes = ['https://graph.microsoft.com/.default']
client = GraphServiceClient(credentials=credentials, scopes=scopes)
```

The above example uses default scopes for [app-only access](https://learn.microsoft.com/en-us/graph/permissions-overview?tabs=http#application-permissions).  If using [delegated access](https://learn.microsoft.com/en-us/graph/permissions-overview#delegated-permissions) you can provide custom scopes:

```py
# Example using sync credentials and delegated access.
from azure.identity import DeviceCodeCredential
from msgraph import GraphServiceClient

credentials = DeviceCodeCredential(
    'CLIENT_ID',
    'TENANT_ID',
)
scopes = ['User.Read', 'Mail.Read']
client = GraphServiceClient(credentials=credentials, scopes=scopes)
```

## 3. Make requests against the service

After you have a **GraphServiceClient** that is authenticated, you can begin making calls against the service. The requests against the service look like [REST API](https://docs.microsoft.com/graph/api/overview?view=graph-rest-1.0).

> **Note**: This SDK offers an asynchronous API by default. Async is a concurrency model that is far more efficient than multi-threading, and can provide significant performance benefits and enable the use of long-lived network connections such as WebSockets. We support popular python async envronments such as `asyncio`, `anyio` or `trio`.


## Documentation and resources

* [Overview](https://docs.microsoft.com/graph/overview)

* [Microsoft Graph website](https://aka.ms/graph)
