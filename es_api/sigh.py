def mod_bar(cls):
    # returns modified class

    def decorate(fcn):
        # returns decorated function

        def new_fcn(self):
            print(self.start_str)
            print(fcn(self))
            print(self.end_str)

        return new_fcn

    cls.bar = decorate(cls.bar)
    for attr in cls.__dict__:  # there's propably a better way to do thi
        if callable(getattr(cls, attr)):
            setattr(cls, attr, decorate(getattr(cls, attr)))
    return cls


@mod_bar
class Test(object):
    def __init__(self):
        self.start_str = "starting dec"
        self.end_str = "ending dec"

    def bar(self):
        return "bar"

    def foo(self):
        return "foo"


a = Test()
