# simpleIOC
Simple Python IOC class

It's a draft of simple solution which will built your objects with all dependencies using annotations

####usage:
```python
from ioc import IOC

class A():
    pass

class B():
    def __init__(self, a: A):
        self.a = a

ioc = IOC()
b = ioc.build(B)
assert isinstance(b.a, A)
```
**build** method produces object of passed class and it's dependencies using annotation of each dependency

To see more examples check `tests.py`

###todo
1. More tests
2. Some real examples