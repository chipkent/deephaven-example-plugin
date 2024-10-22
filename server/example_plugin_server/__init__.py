from typing import List, Any
import json
from deephaven.plugin.object_type import MessageStream, BidirectionalObjectType
from deephaven.plugin import Registration, Callback
from deephaven.plugin import Registration, Callback
from deephaven.plugin.object_type import BidirectionalObjectType, MessageStream
from deephaven.table import Table

# from deephaven import empty_table
# t_debug = empty_table(10).update("X = i")

class ExampleService:

    def echo_string(self, data: str) -> str:
        return f"Echo: {data}"
    
    def echo_table(self, table: Table, data: str) -> Table:
        # return t_debug
        # return table
        return table.update("Echo = `ECHO: ` + data")


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

        message = json.loads(json_string)
        print(f"Received message: {message} {type(message)}")

        result_payload = {}
        result_references = []

        try:
            if message["method"] == "echo_string":
                print(f"Echoing string: {message['data']}")
                result_payload["result"] = self.service.echo_string(message["data"])
                print(f"Result: {result_payload}")
            elif message["method"] == "echo_table":
                print(f"Echoing table: {references[0]}")
                result_payload["result"] = ''
                result_references = [self.service.echo_table(references[0], message["data"])]
            else:
                raise NotImplementedError(f"Unknown message type: {message['method']}")
        except Exception as e:
            print(f"Error processing message: {e}")
            # result_payload["error"] = str(e)
            import traceback
            result_payload["error"] = traceback.format_exc()

        print(f"Sending result: {result_payload}")
        json_string = json.dumps(result_payload).encode("utf-8")
        self.client_connection.on_data(payload=json_string, references=result_references)


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

