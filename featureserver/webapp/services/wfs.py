
import bottle

app = bottle.Bottle()


@app.route('/')
def wfs_list():
    return "moengi wfs"


