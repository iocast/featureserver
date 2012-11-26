
from PostGIS import PostGIS

class PostGISHstore (PostGIS):

    def __init__(self, name, hstore, **kwargs):
        super(PostGISHstore, self).__init__(name, **kwargs)
        self.hstore_attr    = hstore
