from uuid import UUID
from datetime import datetime
import re

def test_email(email: str) -> bool:
    email_regex = "(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|\"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*\")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])"
    if re.match(email_regex, email):
        return True
    else:
        return False


def is_valid_uuid(value):
    try:
        UUID(value)
        return True
    except ValueError:
        return False


# Verify serial number
def verify_serial(serial: str):
    if len(serial) == 10:
        if serial.startswith("SJ") or serial.startswith("SW") or serial.startswith("SP"):
            if (
                serial[2:4] <= str(datetime.now().year)[2:]
                and serial[4:6] >= "01"
                and serial[4:6] <= "12"
                and serial[6:9] <= "999"
                and serial[-1].isupper()
            ):
                return True
    return False
