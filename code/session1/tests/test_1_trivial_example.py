import pytest
# Run this with "pytest -s test_1_trivial_example.py"

def double(x):
    """Double x"""
    return x * 2

def test_double():
    # expected, double, answer could be called whatever you want
    # the only critical bit is the function name starting "test_"
    # plus some assert statements
    expected = 20
    assert double(10) == 20, "Expecting x*2"

    known_input = 10
    answer = double(known_input)
    assert answer == expected, f"Expecting {known_input}*2=={expected} but got {answer}"

    # STUDENTS - IS THIS A USEFUL TEST?
    answer = double(known_input)
    assert expected == 20, f"Expecting {known_input}*2=={expected} but got {answer}"

