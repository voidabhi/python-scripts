
class Proxy:
    def __init__(self, target_object):
        object.__setattr__(self, 'msg', OrderedDict())
        object.__setattr__(self, '_obj', target_object)

    def __getattr__(self, name):
        if name in self.msg:
            self.msg[name] += 1
        else:
            self.msg[name] = 1
        return getattr(self._obj, name)

    def __setattr__(self, name, value):
        if name in self.msg:
            self.msg[name] += 1
        else:
            self.msg[name] = 1
        setattr(self._obj, name, value)
        
class Television:
    def power(self):
        print("Power is on now")

# Usage
tv=Proxy(Television())
tv.power() # Power is on now
print(tv.msg) # { 'power': 1 }
