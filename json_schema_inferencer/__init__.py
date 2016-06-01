#
import argparse
import json

import sys

from .guess_json_schema import from_json
from .guess_json_schema import guess_schema


def parseargs():
    parser = argparse.ArgumentParser(description='Json schema inferencer')
    parser.add_argument('infile', nargs='?', type=argparse.FileType('r'), default=sys.stdin)
    parser.add_argument('-u', '--url', default="")
    args = parser.parse_args()
    return args


def main():
    args = parseargs()
    if args.url:
        json_content = from_json(args.url)
    else:
        json_content = json.loads(args.infile.read())
    print(json.dumps(guess_schema(json_content), indent=2))