import json
import sys
from parse import *

def read(filename):
    with open(filename) as f:
        term = json.load(f)
        return term

json = read(sys.argv[-1])
environment = parse_json(json)
environment["functions"]["main"].call(environment, 0)
