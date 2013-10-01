#!/usr/bin/env python
import sys, os, argparse, json, bottle

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))

from featureserver.webapp.app import get

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="featureserver")
    parser.add_argument('-i', '--host', help="host or ip", required=False, default="localhost")
    parser.add_argument('-p', '--port', help="port", required=False, default=8000)
    parser.add_argument('-d', '--debug', help="enables debugging (boolean switch to trueI)", action='store_true', required=False, default=False)
    
    args = parser.parse_args()
    
    bottle.debug(args.debug)
    bottle.run(app=get(json.load(open(os.path.join(os.path.dirname(__file__), '../featureserver/assets/config/featureserver.json')))), host=args.host, port=args.port, quiet=False, reloader=True)


