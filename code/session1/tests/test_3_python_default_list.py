# TIP `pytest -s test_3_python_default.py` will capture stdout, so any print statements
# you add will be printed to the screen
# TIP `pytest -s -v test_3_python_default.py` will give more vebosity with -v
# If you get stuck start here:
# http://effbot.org/zone/default-values.htm
# and google for:
# "“Least Astonishment” and the Mutable Default Argument"
# TIP this one is horrible if you've not come across it, but you _will_ at some point
# in your career get bitten by this! 

# IMPORTANT TIP try "flake8 test_3_python_default.py" and pay attention "mutable datastructure" warnings...

def accum(item, l=[]):
    """Accumulate items, creating a list if needs be"""
    l.append(item)
    return l


def test():
    assert accum("a") == ["a"]
    assert accum("b") == ["b"]


def test2():
    lst = accum("c")
    assert accum("d", lst) == ["c", "d"]
