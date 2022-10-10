# Use Test Driven Development to build this up
import pytest

EMAIL1 = ("jane@bbc.co.uk", "bbc.co.uk")
EMAIL2 = ("geoff@bbc.co.uk   ", "bbc.co.uk")
EMAIL3 = ("'julie@bbc.co.uk'", "bbc.co.uk")
EMAIL4 = ("'julie@bbc.co.uk' ", "bbc.co.uk")
EMAILS = [EMAIL1, EMAIL2, EMAIL3, EMAIL4]


def get_domain(e):
    return e.strip(' ').replace("'", "").split('@')[1]

def test_str_all():
    for email, domain in EMAILS:
        extracted_domain = get_domain(email)
        assert extracted_domain == domain, f"Extracted domain {extracted_domain} doesn't match the desired domain {domain}"


@pytest.mark.parametrize("email, domain", EMAILS)
def test_str(email, domain):
    assert get_domain(email) == domain
