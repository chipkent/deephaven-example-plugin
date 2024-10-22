import io
from typing import Any, List
from pydeephaven import Table
from pydeephaven.experimental import plugin_client, server_object
import json


class ExampleServiceProxy(server_object.ServerObject):
    def __init__(self, example_plugin: plugin_client.PluginClient):
        self.type_ = example_plugin.type_
        self.ticket = example_plugin.ticket
        self.example_plugin = example_plugin
        # Consume the first (empty) payload from the server
        next(self.example_plugin.resp_stream)

    def echo_string(self, data: str) -> str:
        message = {'method': 'echo_string', 'data': data}
        print(f"Sending message: {message}")
        json_string = json.dumps(message).encode("utf-8")
        print(f"Sending JSON: {json_string} {type(json_string)}")

        decoded = json_string.decode('utf-8')
        print(f"DEBUG: {decoded} {type(decoded)}")
        decoded2 = json.loads(decoded)
        print(f"DEBUG2: {decoded2} {type(decoded2)}")


        self.example_plugin.req_stream.write(json_string, [])
        result_bytes, result_references = next(self.example_plugin.resp_stream)

        result_json = json.loads(result_bytes.decode("utf-8"))

        if 'error' in result_json:
            raise Exception(result_json['error'])

        return result_json['result']
    
    def echo_table(self, table: Table, label: str) -> Table:
        message = {'method': 'echo_table', 'data': label}
        json_string = json.dumps(message).encode("utf-8")
        self.example_plugin.req_stream.write(json_string, [table])
        result_bytes, result_references = next(self.example_plugin.resp_stream)

        result_json = json.loads(result_bytes.decode("utf-8"))

        if 'error' in result_json:
            raise Exception(result_json['error'])
        
        return result_references[0].fetch()






