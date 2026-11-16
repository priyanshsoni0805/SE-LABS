"""Highway toll helpers, hardened against invalid input (Lab 7 fixed version).

Every public function validates its input and returns None for anything
invalid, instead of raising an unexpected exception. Bugs found by fuzzing
with Hypothesis that are fixed here:

parse_plate
  - None / non-string input          -> AttributeError on .split
  - wrong number of '-' parts        -> ValueError (unpacking)
  - non-numeric district or number   -> ValueError from int()
  - int() accepted ' 5', '+5', '1_0' and non-ASCII digits such as '٥'
  - empty or non-letter state/series parts were accepted silently

trip_cost
  - None / non-string input          -> AttributeError on .lower
  - no 'x' or more than one 'x'      -> ValueError (unpacking)
  - non-numeric parts                -> ValueError from int()
  - negative or zero trips accepted ('-3x150', '0x150')
  - extremely long digit strings     -> ValueError (int max digits) / huge results

axle_class
  - None                             -> TypeError from int()
  - non-numeric text                 -> ValueError from int()
  - floats silently truncated (int(2.9) == 2 -> 'car')
  - bool accepted (True -> 1)
  - 0, 1 and negative axle counts were classed as 'truck'
"""

MAX_TRIPS = 1000          # sensible upper bound for one billing request
MAX_RATE = 100000         # highest toll rate (INR) accepted per trip
MAX_AXLES = 20            # largest axle count the classifier accepts


def _is_ascii_digits(s, min_len=1, max_len=None):
    """True if s is non-empty and made only of ASCII digits 0-9 (length-limited)."""
    if not isinstance(s, str) or len(s) < min_len:
        return False
    if max_len is not None and len(s) > max_len:
        return False
    return all('0' <= ch <= '9' for ch in s)


def _is_ascii_letters(s, min_len=1, max_len=None):
    """True if s is made only of ASCII letters A-Z / a-z (length-limited)."""
    if not isinstance(s, str) or len(s) < min_len:
        return False
    if max_len is not None and len(s) > max_len:
        return False
    return all(('A' <= ch <= 'Z') or ('a' <= ch <= 'z') for ch in s)


def parse_plate(plate):
    """Parse an Indian-style plate 'SS-DD-XX-NNNN' (e.g. 'KA-05-AB-1234').

    Returns (STATE, district:int, number:int) or None if the plate is invalid.
    """
    if not isinstance(plate, str):
        return None
    parts = plate.strip().split('-')
    if len(parts) != 4:
        return None
    state, district, series, number = parts
    if not _is_ascii_letters(state, 2, 2):
        return None
    if not _is_ascii_digits(district, 1, 2):
        return None
    if not _is_ascii_letters(series, 1, 3):
        return None
    if not _is_ascii_digits(number, 1, 4):
        return None
    district_no, plate_no = int(district), int(number)
    if district_no == 0 or plate_no == 0:
        return None
    return state.upper(), district_no, plate_no


def trip_cost(text):
    """Price 'COUNTxRATE' (e.g. '3x150' -> 450).

    COUNT must be 1..MAX_TRIPS and RATE 0..MAX_RATE, both plain ASCII digits.
    Returns the integer cost or None if the input is invalid.
    """
    if not isinstance(text, str):
        return None
    parts = text.strip().lower().split('x')
    if len(parts) != 2:
        return None
    count, rate = (p.strip() for p in parts)
    if not _is_ascii_digits(count, 1, 4) or not _is_ascii_digits(rate, 1, 6):
        return None
    count, rate = int(count), int(rate)
    if not (1 <= count <= MAX_TRIPS) or not (0 <= rate <= MAX_RATE):
        return None
    return count * rate


def axle_class(axles):
    """Classify a vehicle by axle count: 2 -> 'car', 3-4 -> 'truck', 5+ -> 'heavy'.

    Accepts an int or a string of ASCII digits. Returns None for anything
    else, or for counts outside 2..MAX_AXLES.
    """
    if isinstance(axles, bool):
        return None
    if isinstance(axles, int):
        n = axles
    elif isinstance(axles, str) and _is_ascii_digits(axles.strip(), 1, 3):
        n = int(axles.strip())
    else:
        return None
    if n < 2 or n > MAX_AXLES:
        return None
    if n == 2:
        return 'car'
    if n <= 4:
        return 'truck'
    return 'heavy'


def _ask(prompt):
    try:
        return input(prompt)
    except EOFError:
        return None


def main():
    print("==== Running parse_plate ====")
    user_input = _ask("Enter a plate (e.g. KA-05-AB-1234): ")
    result = parse_plate(user_input)
    if result is None:
        print("Invalid plate. Expected format like KA-05-AB-1234.")
    else:
        print("State, District and Number:", result)

    print("\n==== Running trip_cost ====")
    user_input = _ask("Enter trips x rate (e.g. 3x150): ")
    result = trip_cost(user_input)
    if result is None:
        print(f"Invalid input. Expected COUNTxRATE with 1-{MAX_TRIPS} trips and rate 0-{MAX_RATE}.")
    else:
        print("Trip Cost:", result)

    print("\n==== Running axle_class ====")
    user_input = _ask("Enter an axle count (e.g. 3): ")
    result = axle_class(user_input)
    if result is None:
        print(f"Invalid axle count. Enter a whole number from 2 to {MAX_AXLES}.")
    else:
        print("Vehicle Class:", result)


if __name__ == "__main__":
    main()
