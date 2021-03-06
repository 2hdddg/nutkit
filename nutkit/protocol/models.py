"""
All models are sent from backend as:
    {
        name: <class name>
        data: {
            <all instance variables>
        }
    }
"""

class Driver:
    """
    data: {id: 'driver id'}
    """
    def __init__(self, id):
        self.id = id


class Session:
    """
    data: {id: 'session id'}
    """
    def __init__(self, id):
        self.id = id


class Result:
    """
    data: {id: 'result id'}
    TODO: keys: ['field1', 'field2']
    """
    def __init__(self, id):
        self.id = id


class Record:
    """
    data: {values: [CypherX, CypherY] }
    """
    def __init__(self, values=None):
        self.values = values


class NullRecord:
    """
    data: null
    """
    def __init__(self):
        pass


class RetryableTry:
    def __init__(self, id):
        self.id = id


class RetryableDone:
    def __init__(self):
        pass

class Error:
    def __init__(self, id):
        pass


class CypherNull:
    def __init__(self, value=None):
        pass

    def __str__(self):
        return "<null>"


class CypherList:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        v = []
        for x in self.value:
            v.append(str(x))
        return "List {}".format(v)


class CypherMap:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        v = {}
        for k in self.value:
            v[k] = str(self.value[k])
        print(self.value)
        return "Map {}".format(v)


class CypherInt:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class CypherString:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return self.value


class Node:
    def __init__(self, id, labels, props):
        self.id = id
        self.labels = labels
        self.props = props

    def __str__(self):
        return "Node (id={}, labels={}), props={}".format(
            self.id, self.labels, self.props)


class BaseError(Exception):
    """ Base class for all types of errors, should not be sent from backend

    All models inheriting from this will be thrown as exceptions upon retrieval from backend.
    """
    pass


class DriverError(BaseError):
    """ Base class for all kind of driver errors that is NOT a backend specific error
    """
    def __init__(self, id):
        self.id = id


class BackendError(BaseError):
    """ Sent by backend when there is an internal error in the backend, not the driver.  """
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

