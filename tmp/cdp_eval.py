import websocket, json, time, sys

ws_url = sys.argv[1]
timeout = int(sys.argv[2]) if len(sys.argv) > 2 else 15
msg = sys.argv[3] if len(sys.argv) > 3 else ''

ws = websocket.create_connection(ws_url, timeout=timeout)
# Enable Runtime
ws.send(json.dumps({"id":1,"method":"Runtime.enable"}))
ws.recv()

# Evaluate expression
ws.send(json.dumps({"id":2,"method":"Runtime.evaluate","params":{"expression": msg, "returnByValue": True}}))
result = json.loads(ws.recv())
ws.close()

if 'result' in result and 'result' in result['result']:
    obj = result['result']['result']
    print(obj.get('value', ''))
elif 'error' in result.get('result', {}):
    print('ERROR:', result['result']['error'].get('text', ''))
else:
    print(json.dumps(result, indent=2))
