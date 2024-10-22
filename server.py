from deephaven_server import Server

server = Server(
    jvm_args=["-Xmx4g", "-Dauthentication.psk=YOUR_PASSWORD_HERE"]
)
server.start()

import sys
from example_plugin_server import ExampleService

example_service = ExampleService()


print("Press Control-C to exit")

try:
    while True:
        input()
except KeyboardInterrupt:
    print("Exiting Deephaven...")
    sys.exit(0)