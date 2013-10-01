import bottle

app = bottle.Bottle()


@app.route('/')
def rest_list():
    return "moengi rest"

