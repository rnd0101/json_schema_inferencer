#
import argparse
import json

from json_schema_inferencer.guess_json_schema import from_json
from json_schema_inferencer.guess_json_schema import guess_schema


def parseargs():
    parser = argparse.ArgumentParser(description='Json schema inferencer')
    parser.add_argument('-u', '--url', default="", required=True)
    args = parser.parse_args()
    return args


def main():
    args = parseargs()
    json_content = from_json(args.url)
    print(json.dumps(guess_schema(json_content), indent=2))