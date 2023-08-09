import os
from datetime import datetime
from dotenv import load_dotenv
from minio import error
from moviematchr.services.data_storage.post_a_binary_file_in_storage import (
    post_a_binary_file_in_storage,
)
from moviematchr.services.data_storage.get_from_storage import (
    get_from_storage,
)

load_dotenv()

LAST_SERIAL = os.getenv("LAST_SERIAL")

alphabet = [
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "A",
    "B",
    "C",
    "D",
    "E",
    "F",
    "G",
    "H",
    "I",
    "J",
    "K",
    "L",
    "M",
    "N",
    "O",
    "P",
    "Q",
    "R",
    "S",
    "T",
    "U",
    "V",
    "W",
    "X",
    "Y",
    "Z",
]


async def generate_new_serial_number():
    new_serial = "YB"
    # Get the two last numbers of the year
    new_serial += str(datetime.now().year)[-2:]
    # Get the two first numbers of the month
    new_serial += str(datetime.now().month).zfill(2)

    try:
        file = get_from_storage(LAST_SERIAL)
        last_serial = file.data.decode("utf-8")

        if last_serial[:6] == new_serial:
            new_number = generate_new_number(str(last_serial[6:9]))
            new_serial += new_number + "E"

        else:
            new_serial += str(1).zfill(3) + "E"

        post_a_binary_file_in_storage(new_serial, LAST_SERIAL)

    except error.S3Error:
        new_serial += str(1).zfill(3) + "E"
        post_a_binary_file_in_storage(new_serial, LAST_SERIAL)

    return new_serial


def generate_new_number(last: str) -> str:
    if last == "9ZZ":
        raise ValueError("Too many numbers generated")

    if last == "99Z":
        return "9A0"

    if last[-1] != "Z":
        return last[:-1] + alphabet[alphabet.index(last[-1]) + 1]

    if last[-2] != "Z":
        if last[-2].isnumeric():
            if int(last[-2]) < 9:
                return last[:-2] + str(int(last[-2]) + 1) + "0"
            else:
                return last[:-2] + "A0"
        else:
            return last[:-2] + alphabet[alphabet.index(last[-2]) + 1] + "0"

    if last[0] != "9":
        return alphabet[alphabet.index(last[0]) + 1] + "00"

    raise ValueError("Too many numbers generated")
