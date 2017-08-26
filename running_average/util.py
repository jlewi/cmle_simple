import json

def PrettyFormat(d):
  return json.dumps(d, sort_keys=True,
                    indent=2, separators=(',', ': '))