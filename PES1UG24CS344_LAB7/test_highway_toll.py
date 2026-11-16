from hypothesis import given, settings, strategies as st
from highway_toll import parse_plate, trip_cost, axle_class

# Any junk a user (or attacker) could pass in: text, None, numbers, bools, lists...
ANY_INPUT = st.one_of(
    st.text(),
    st.none(),
    st.integers(),
    st.floats(allow_nan=True, allow_infinity=True),
    st.booleans(),
    st.binary(),
    st.lists(st.text(), max_size=4),
)

UPPER = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LETTERS = UPPER + UPPER.lower()


# ===========================================================================
# 1. parse_plate
# ===========================================================================
@settings(max_examples=300)
@given(st.text() | st.none())
def test_parse_plate_no_crash(s):
    try:
        result = parse_plate(s)
    except Exception as e:
        assert False, f"parse_plate crashed on {s!r} with: {type(e).__name__}: {e}"
    assert result is None or (isinstance(result, tuple) and len(result) == 3)


@given(ANY_INPUT)
def test_parse_plate_no_crash_any_type(s):
    try:
        parse_plate(s)
    except Exception as e:
        assert False, f"parse_plate crashed on {s!r} with: {type(e).__name__}: {e}"


@given(
    state=st.text(alphabet=LETTERS, min_size=2, max_size=2),
    district=st.integers(min_value=1, max_value=99),
    series=st.text(alphabet=LETTERS, min_size=1, max_size=3),
    number=st.integers(min_value=1, max_value=9999),
)
def test_parse_plate_valid_plates_round_trip(state, district, series, number):
    plate = f"{state}-{district:02d}-{series}-{number:04d}"
    assert parse_plate(plate) == (state.upper(), district, number)


@given(st.lists(st.text(alphabet=LETTERS + "0123456789", min_size=1, max_size=4), min_size=1, max_size=7)
       .filter(lambda parts: len(parts) != 4))
def test_parse_plate_wrong_number_of_parts_is_rejected(parts):
    assert parse_plate("-".join(parts)) is None


@given(st.sampled_from(["KA-٠٥-AB-1234", "KA- 5-AB-1234", "KA-+5-AB-1234", "KA-0_5-AB-1234",
                        "KA-05-AB-12_34", "K1-05-AB-1234", "KA-05-12-1234", "--AB-1234", "KA-05-AB-"]))
def test_parse_plate_rejects_tricky_numbers_and_parts(plate):
    assert parse_plate(plate) is None


# ===========================================================================
# 2. trip_cost
# ===========================================================================
@settings(max_examples=300)
@given(st.text() | st.none())
def test_trip_cost_no_crash(s):
    try:
        result = trip_cost(s)
    except Exception as e:
        assert False, f"trip_cost crashed on {s!r} with: {type(e).__name__}: {e}"
    assert result is None or isinstance(result, int)


@given(ANY_INPUT)
def test_trip_cost_no_crash_any_type(s):
    try:
        trip_cost(s)
    except Exception as e:
        assert False, f"trip_cost crashed on {s!r} with: {type(e).__name__}: {e}"


@given(count=st.integers(min_value=1, max_value=1000),
       rate=st.integers(min_value=0, max_value=100000),
       sep=st.sampled_from(["x", "X"]))
def test_trip_cost_valid_input_is_count_times_rate(count, rate, sep):
    assert trip_cost(f"{count}{sep}{rate}") == count * rate


@given(count=st.integers(max_value=0), rate=st.integers(min_value=0, max_value=1000))
def test_trip_cost_rejects_zero_or_negative_trips(count, rate):
    assert trip_cost(f"{count}x{rate}") is None


@given(count=st.integers(min_value=1001, max_value=10**12), rate=st.integers(min_value=0, max_value=1000))
def test_trip_cost_rejects_too_many_trips(count, rate):
    assert trip_cost(f"{count}x{rate}") is None


def test_trip_cost_rejects_huge_digit_strings():
    # int() refuses strings longer than 4300 digits on Python 3.11+, crashing the old code
    huge = "9" * 5000
    assert trip_cost(f"{huge}x{huge}") is None


# ===========================================================================
# 3. axle_class
# ===========================================================================
@settings(max_examples=300)
@given(st.text() | st.none())
def test_axle_class_no_crash(s):
    try:
        result = axle_class(s)
    except Exception as e:
        assert False, f"axle_class crashed on {s!r} with: {type(e).__name__}: {e}"
    assert result in (None, "car", "truck", "heavy")


@given(ANY_INPUT)
def test_axle_class_no_crash_any_type(s):
    try:
        axle_class(s)
    except Exception as e:
        assert False, f"axle_class crashed on {s!r} with: {type(e).__name__}: {e}"


@given(st.integers())
def test_axle_class_integer_mapping(n):
    expected = None
    if 2 <= n <= 20:
        expected = "car" if n == 2 else "truck" if n <= 4 else "heavy"
    assert axle_class(n) == expected
    if 0 <= n:
        assert axle_class(str(n)) == expected     # same answer for digit strings


@given(st.floats(allow_nan=True, allow_infinity=True))
def test_axle_class_rejects_floats(f):
    # int(2.9) == 2 used to be classed as 'car'; floats are now rejected outright
    assert axle_class(f) is None


def test_axle_class_rejects_bools():
    assert axle_class(True) is None
    assert axle_class(False) is None
