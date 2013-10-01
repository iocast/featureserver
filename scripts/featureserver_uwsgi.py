import sys, os

sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from featureserver.webapp.app import get

application = get()
