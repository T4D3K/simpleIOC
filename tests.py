from ioc import IOC, Singleton


class A:
    pass


class B:
    def __init__(self, ioc_a: A):
        self.a = ioc_a


class C(B):
    pass


class D:
    pass


class E:
    def __init__(self, ioc_d: D, ioc_c: C, some_def_value='default'):
        self.d = ioc_d
        self.c = ioc_c
        self.default = some_def_value


class F:
    def __init__(self, l: list):
        self.l = l


def test_default_build():
    ioc = IOC()
    e = ioc.build(E)
    assert isinstance(e, E)
    assert isinstance(e.d, D)
    assert isinstance(e.c, C)
    assert isinstance(e.c.a, A)


def test_default_value():
    ioc = IOC()
    e = ioc.build(E)
    assert e.default == 'default'


def test_override_params_by_global_context():
    ioc = IOC()
    e = ioc.build(E, {'some_def_value': 'my_value', 'ioc_a': 'it is not an A object now'})
    assert e.default == 'my_value'
    assert e.c.a == 'it is not an A object now'


def test_replace_arguments_for_one_class():
    ioc = IOC({
        E: {'ioc_c': B, 'ioc_d': C}
    })
    e = ioc.build(E)
    assert isinstance(e.c, B)
    assert isinstance(e.d, C)


def test_not_initialized_singleton():
    ioc = IOC({
        E: {'ioc_c': B, 'ioc_d': C},
        A: Singleton(A)
    })
    e = ioc.build(E)
    assert e.c.a is e.d.a


def test_initialized_singleton():
    ioc = IOC({
        E: {'ioc_c': B, 'ioc_d': C},
        A: A()
    })
    e = ioc.build(E)
    assert e.c.a is e.d.a


def test_replaced_by_something_else():
    ioc = IOC({
        E: {'ioc_c': B, 'ioc_d': C},
        A: 1
    })
    e = ioc.build(E)
    assert e.c.a == 1


def test_empty_mutable():
    ioc = IOC()
    f1 = ioc.build(F)
    f2 = ioc.build(F)
    f3 = ioc.build(F, {'l': [1, 2, 3]})
    assert f1.l == []
    assert f2.l == []
    assert f1.l is not f2.l
    assert f3.l == [1, 2, 3]

def test_runtime_change_in_conf():
    ioc = IOC()
    e1 = ioc.build(E)
    ioc.conf[E] = {'ioc_c': B}
    e2 = ioc.build(E)
    ioc.reset_to_default_conf()
    e3 = ioc.build(E)
    assert isinstance(e1.c, C)
    assert isinstance(e2.c, B)
    assert isinstance(e3.c, C)

def test_configure_part_of_class():
    ioc = IOC({E: {'ioc_c': B}})
    e = ioc.build(E)
    assert isinstance(e.c, B)
    assert isinstance(e.d, D)


