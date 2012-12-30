

class Operator(object):
    def __init__(self, attribute, operator, **kwargs):
        super(Operator, self).__init__(**kwargs)
        
        self._attribute     = attribute
        self._operator        = operator
        
        for key, value in kwargs.iteritems():
            setattr(self, key, value)

    @property
    def attribute(self):
        return self._attribute
    @property
    def operator(self):
        return self._operator



class Constraint(Operator):
    def __init__(self, attribute, value, operator = 'eq', **kwargs):
        super(Constraint, self).__init__(attribute, operator, **kwargs)
    
        self._value = value
            
    @property
    def value(self):
        return self._value

class Sort(Operator):
    def __init__(self, attribute, operator = 'ASC', **kwargs):
        super(Sort, self).__init__(attribute, operator, **kwargs)



