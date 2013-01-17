

class Operator(object):
    def __init__(self, attribute, operator, value, **kwargs):
        super(Operator, self).__init__(**kwargs)
        
        self._attribute     = attribute
        self._operator      = operator
        self._value         = value
        
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    @property
    def attribute(self):
        return self._attribute
    @property
    def operator(self):
        return self._operator
    @property
    def value(self):
        return self._value


class BoundingBox(Operator):
    def __init__(self, value, **kwargs):
        super(BoundingBox, self).__init__(None, 'bbox', value, **kwargs)

class Constraint(Operator):
    def __init__(self, attribute, value, operator = 'eq', **kwargs):
        super(Constraint, self).__init__(attribute, operator, value, **kwargs)

class Sort(Operator):
    def __init__(self, attribute, operator = 'ASC', **kwargs):
        super(Sort, self).__init__(attribute, operator, None, **kwargs)



