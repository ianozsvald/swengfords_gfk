import pytest
import math

# STUDENTS this is an example of
# Test Driven Development
# The test are written, supporting code is only lightly written
# so your tests will faily - but you can use these to "fill in the blanks"
# as you puzzle your way to a working solution

# run this with:
# `pytest homework_is_prime.py`
# and note that your tests will FAIL
# that's good - you have to use a Test Driven Development style
# to fill in the `is_prime` function that's below with
# code to match the unit tests
# don't worry - the notes below will guide you. Get as far as you can.

# start with the _simplest solution_ possible
# and the simplest solution will be that is_prime(2) will `return True`

# Primality means that there are no integer factors, a factor is a number
# that divides your number evenly. 2 is a factor of 4 (and 6, 8, 1000, ...)
# and 9 is a factor of 18, 27 etc. 3 is a factor of 9.

# now test for primes in a simple way:
#  if n % 2 == 0 then is_prime is False # i.e. if n / 2 has 0 remainder then
# n is divisible by 2 so it isn't a prime (examples include 2, 4, 6, ..., 100, ...1000)
#  if n % 3 == 0 then is_prime is False (examples include 3, 6, 9, 90, 1800)
#  if n % 4 == 0 then is_prime is False... 
# so if n is 5, n%2 and n%3 and n%4 each give a number != 0 so is_prime(5) is True

# now:
# write a for loop with `idx` that checks up to n-1 using the mod (%) operator,
# if n%idx==0 then is_prime must be False
# if for all n up to n-1, n%idx!=0 then is_prime is True and we've found a prime
# return True for is_prime if the n%loop_counter==0 are all False
# primes include 2, 3, 5, 7, 11
# non-primes include 4, 6, 8, 9, 10, 12

# next add some exception handling, raise a ValueError if n<=1 as primes
# are only defined for n >= 2
# you can raise a ValueError with a useful message with:
# `raise ValueError(f'{n} must be >= 2 for a prime test')

# bonus if you like math puzzles...
# finally now that you've got a good prime testing solution, note that it
# is slow. if instead you check not up to n-1 but up to
# int(math.sqrt(n))+1
# then you'll have a much shorter testing range and testing for large primes
# wil be quicker
# if you make the above change and confirm that your tests still pass, you've
# used your tests to enable you to successfully refactor your code with a
# better (faster in this case) solution that is just as correct as the earlier
# version


def is_prime(n):
    # STUDENT expand this function please with a for loop as
    # described above, you only need to work on this function
    # and test it with pytest as described above
    return True


def tests_main():
    # STUDENT don't touch this function...
    assert is_prime(2) is True
    assert is_prime(3) is True
    assert is_prime(4) is False

    items = [
        (3, True),
        (5, True),
        (6, False),
        (9, False),
        (102241, True),
        (102243, False),
        (15485863, True),
    ]
    for item, answer in items:
        assert is_prime(item) is answer


def test_exception():
    # STUDENT don't touch this function...
    with pytest.raises(ValueError):
        is_prime(0)
    with pytest.raises(ValueError):
        is_prime(1)
    with pytest.raises(ValueError):
        is_prime(-1)
