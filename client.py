from pydeephaven import Session
from example_plugin_client import ExampleServiceProxy

session = Session(
    auth_type="io.deephaven.authentication.psk.PskAuthenticationHandler",
    auth_token="YOUR_PASSWORD_HERE",
)

print(f"KEYS: {session.exportable_objects.keys()}")

service_ticket = session.exportable_objects["example_service"]
service_plugin = session.plugin_client(service_ticket)

shell = ExampleServiceProxy(service_plugin)

print("Echoing string...")
echo_result = shell.echo_string("Hello, world!")
print(echo_result)

print("Echoing table...")
t = session.empty_table(10).update("Original = `Hello, world!`")

table_result = shell.echo_table(t, "Hello, world!")
print(f"Table result: {table_result} {type(table_result)}")
print("Table result:")
print(table_result.to_arrow().to_pandas())
