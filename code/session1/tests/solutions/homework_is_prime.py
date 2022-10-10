import pytest
import math


# to run coverage without running tests
# coverage run homework_is_prime.py
# this will generate a .coverage folder
# coverage report
# will make a text report
# coverage html
# firefox htmlcov/index.html
# will give a graphical report
# coverage erase
# will remove data (also delete the htmlcov folder)

# to check our test coverage
# coverage run -m pytest homework_is_prime.py
# coverge html
# (OR pytest --cov=. --cov-report=html homework_is_prime.py)
# firefox htmlcov/index.html

# identifying dead code with vulture
# vulture homework_is_prime.py
# will identify unused functions and math import (if commented out)


# we have this function to show how coverage works
def another_function_that_is_not_tested():
    1 / 0
    return False


def is_prime(n):
    if n < 2:
        raise ValueError(f"n must be >= 2 and it currently is {n}")
    upper = n-1 # really slow!
    #upper = (n // 2) + 1 # based on observation that if 2 is not a factor, there's
    # no point going more than half way up the range
    #upper = int(math.sqrt(n)) + 1 # faster upper bound
    print(f"For {n} our upper bound is {upper}")  # use -s in pytest to see stdout
    for idx in range(2, upper):
        if n % idx == 0:
            return False
    return True


def tests_main():
    assert is_prime(2) == True
    assert is_prime(3) == True
    assert is_prime(4) == False

    items = [(3, True), (5, True), (6, False), (9, False), (102241, True), (102243, False), (15485863, True)]
    for item, answer in items:
        assert is_prime(item) == answer


def test_exception():
    with pytest.raises(ValueError):
        is_prime(0)
    with pytest.raises(ValueError):
        is_prime(1)
    with pytest.raises(ValueError):
        is_prime(-1)

if __name__ == "__main__":
    is_prime(22)
