# deephaven-example-plugin
An example Deephaven plugin.  This plugin allows a client to call methods on a server-side object.

Relevant code:
* [./server](./server/): The server-side plugin.
* [./server.py](./server.py): A script to setup and run the server.
* [./client](./client/): The client-side plugin.
* [./client.py](./client.py): A script to setup and run the client.

In one console run:
```bash
./server.py
```
and in another console run:
```bash
./client.py
```

