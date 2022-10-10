# Use Test Driven Development to build this up
# When you run this you'll get 4 failures, so you want to solve one at a time
# Start by building up string processing (e.g. with split) in get_domain
# to incrementally solve each of the 4 patterns
# use "pytest -s" to get stdout printed
# TIPS - you will need to split the string, then strip it, then replace 
# the extraneous quotes
import pytest

# each pair shows an email address and the domain we'd like to extract
# where the email might have spurious quotes or whitespace
# which you need to deal with
EMAIL1 = ("jane@bbc.co.uk", "bbc.co.uk")
EMAIL2 = ("geoff@bbc.co.uk   ", "bbc.co.uk")
EMAIL3 = ("'julie@bbc.co.uk'", "bbc.co.uk")
EMAIL4 = ("'julie@bbc.co.uk' ", "bbc.co.uk")
EMAILS = [EMAIL1, EMAIL2, EMAIL3, EMAIL4]


def get_domain(e):
    # simplest implementation but wrong
    print(f"We want to get domain for :{e}:") # print for your visual debugging
    return e

# STUDENTS what is going on here?
# WHY might this be helpful when we're building or reading tests?
@pytest.mark.parametrize("email, domain", EMAILS)
def test_str(email, domain):
    assert get_domain(email) == domain
