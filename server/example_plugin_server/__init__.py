from typing import List, Any
import json
from deephaven.plugin.object_type import MessageStream, BidirectionalObjectType
from deephaven.plugin import Registration, Callback
from deephaven.plugin import Registration, Callback
from deephaven.plugin.object_type import BidirectionalObjectType, MessageStream
from deephaven.table import Table

class ExampleService:

    def echo_string(self, data: str) -> str:
        return f"Echo: {data}"
    
    def echo_table(self, table: Table, data: str) -> Table:
        return table.update("Label = `{data}`")


class ExampleServiceConnection(MessageStream):
    def __init__(self, service: ExampleService, client_connection: MessageStream):
        print("CREATING: ExampleServiceConnection")

        self.service = service
        self.client_connection = client_connection
        # Send an empty payload to the client to acknowledge successful connection
        self.client_connection.on_data(b'', [])

        print("CREATED: ExampleServiceConnection")

    def on_data(self, payload: bytes, references: List[Any]):
        print("Received data from client: ", payload, type(payload), len(payload))

        payload = bytes(payload)[:]
        print(f"Received data from client (copy): {payload} {type(payload)}")

        json_string = payload.decode("utf-8")
        # json_string = bytes(payload).decode("utf-8")
        print(f"Received JSON: {json_string} {type(json_string)}")



        # debug = bytes(payload)
        # print(f"DEBUG: {debug} {type(debug)}")

        # try:
        #     decode = debug.decode('utf-8')
        #     print(f"DEBUG2: {decode} {type(decode)}")

        #     msg = json.loads(decode)
        #     print(f"DEBUG3: {msg} {type(msg)}")
        # except UnicodeDecodeError:
        #     print(f"DEBUG-X: failed")


        # json_string = bytes(iter(payload)).decode("utf-8")
        # print(f"Received JSON: {json_string}")


        # try:
        #     message = json.loads(json_string)
        # except json.JSONDecodeError:
        #     print(f"Error decoding JSON:")
        #     return

        message = json.loads(json_string)
        print(f"Received message: {message} {type(message)}")

        try:
            print(f"message['method']: {message['method']}")
        except KeyError:
            print(f"Error: message['method'] not found")

        try:
            print(f"message['data']: {message['data']}")
        except KeyError:
            print(f"Error: message['data'] not found")

        if message["method"] == "echo_string":
            print(f"Echoing string: {message['data']}")
            result = self.service.echo_string(message["data"])
            print(f"Result: {result}")
            self.client_connection.on_data(payload=result.encode('utf-8'), references=[])
        elif message["method"] == "echo_table":
            print(f"Echoing table: {references[0]}")
            result = self.service.echo_table(references[0], message["data"])
            print(f"Result: {result}")
            self.client_connection.on_data(payload=b'', references=[result])
        else:
            print(f"Unknown message type: {message['message_type']}")
            return
            # raise NotImplementedError(f"Unknown message type: {message['message_type']}")

    def on_close(self):
        print("Client connection closed.")


class ExampleServiceObjectType(BidirectionalObjectType):

    def __init__(self):
        print(f"CREATING: ExampleServiceObjectType")
        super().__init__()
        print(f"CREATED: ExampleServiceObjectType")


    @property
    def name(self) -> str:
        print("Getting name of ExampleService")
        return "ExampleService"

    def is_type(self, object) -> bool:
        print(f"Checking if {object} is an ExampleService: {isinstance(object, ExampleService)}")
        return isinstance(object, ExampleService)

    def create_client_connection(self, obj: ExampleService, connection: MessageStream) -> MessageStream:
        print("CREATING: ExampleServiceConnection")
        conn = ExampleServiceConnection(obj, connection)
        print("CREATED:ExampleServiceConnection")
        return conn


class ExampleServicePluginRegistration(Registration):
    @classmethod
    def register_into(cls, callback: Callback) -> None:
        print("START: Registering ExampleServicePlugin")
        callback.register(ExampleServiceObjectType)
        print("END: Registering ExampleServicePlugin")

