import json, re, copy, uuid

with open("data/raw/mercado_libre_mock.json", encoding="utf-8") as f:
    config = json.load(f)

route_vendedores = None
idx = None
for i, r in enumerate(config["routes"]):
    if r.get("endpoint") == "users/vendedores":
        route_vendedores = r
        idx = i
        break

body = route_vendedores["responses"][0]["body"]

# Extract each case block: {{# case N }} ... {{/ case }}
pattern = r"\{\{#\s*case\s+(\d+)\s*\}\}(.*?)\{\{/\s*case\s*\}\}"
matches = re.findall(pattern, body, re.DOTALL)

new_responses = []
for case_val, raw_json in matches:
    raw_json = raw_json.strip()
    raw_json = re.sub(r",\s*$", "", raw_json)  # trailing comma
    parsed = json.loads(raw_json)
    resp = {
        "uuid": str(uuid.uuid4()),
        "body": json.dumps(parsed, ensure_ascii=False),
        "latency": 0,
        "statusCode": 200,
        "label": f"Vendedor {case_val}",
        "headers": [],
        "bodyType": "INLINE",
        "filePath": "",
        "databucketID": "",
        "sendFileAsBody": False,
        "rules": [
            {
                "target": "query",
                "modifier": "id",
                "value": case_val,
                "inject": False,
                "regex": False
            }
        ],
        "rulesOperator": "OR",
        "disableTemplating": True,
        "fallbackTo404": False,
        "default": False,
        "crudKey": "id",
        "callbacks": []
    }
    new_responses.append(resp)

# default / fallback
default_resp = {
    "uuid": str(uuid.uuid4()),
    "body": json.dumps({"error": "Vendedor no encontrado. Por favor usa un ID del 1 al 5."}, ensure_ascii=False),
    "latency": 0,
    "statusCode": 200,
    "label": "Error - ID no valido",
    "headers": [],
    "bodyType": "INLINE",
    "filePath": "",
    "databucketID": "",
    "sendFileAsBody": False,
    "rules": [],
    "rulesOperator": "OR",
    "disableTemplating": True,
    "fallbackTo404": False,
    "default": True,
    "crudKey": "id",
    "callbacks": []
}
new_responses.append(default_resp)

route_vendedores["responses"] = new_responses

with open("data/raw/mercado_libre_mock.json", "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2, ensure_ascii=False)

print(f"Transformacion completada: {len(new_responses)-1} vendedores + 1 default")
