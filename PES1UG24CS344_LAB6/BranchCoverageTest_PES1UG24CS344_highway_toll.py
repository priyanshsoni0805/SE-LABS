"""Branch coverage tests for highway_toll.py
Priyansh Soni - PES1UG24CS344

Goal: >= 90% branch coverage. Every decision (if / for) is driven both ways:
axles < 2, axles in BASE_TOLL, is_peak, has_fastag, axles == 2, vehicle in EXEMPT,
the trips loop (zero and many iterations), cost > pass_price and cost == pass_price.
"""
import pytest
from highway_toll import toll_for, toll_charge, pass_advice


# ---------------------------------------------------------------------------
# Example test cases (given)
# ---------------------------------------------------------------------------
def test_ambulance_is_exempt():
    assert toll_charge("ambulance", 2, False, False) == 0


def test_two_axle_base_toll():
    assert toll_for(2, False, False) == 100


# ---------------------------------------------------------------------------
# toll_for: invalid axle count  (branch: axles < 2 -> True)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("axles", [1, 0, -3])
def test_toll_for_rejects_fewer_than_two_axles(axles):
    with pytest.raises(ValueError, match="invalid axle count"):
        toll_for(axles, False, False)


# ---------------------------------------------------------------------------
# toll_for: base toll lookup  (branch: axles in BASE_TOLL -> True / False)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("axles, expected", [
    (2, 100),   # in table
    (3, 150),   # in table
    (4, 250),   # in table
    (5, 400),   # not in table -> default 400
    (9, 400),   # not in table -> default 400
])
def test_toll_for_base_rates(axles, expected):
    assert toll_for(axles, False, False) == expected


# ---------------------------------------------------------------------------
# toll_for: peak surcharge  (branch: is_peak -> True)
# ---------------------------------------------------------------------------
@pytest.mark.parametrize("axles, expected", [
    (2, 125.0),   # 100 * 1.25
    (3, 187.5),   # 150 * 1.25
    (5, 500.0),   # 400 * 1.25
])
def test_toll_for_peak_surcharge(axles, expected):
    assert toll_for(axles, True, False) == expected


# ---------------------------------------------------------------------------
# toll_for: FASTag discount  (branch: has_fastag -> True, axles == 2 True / False)
# ---------------------------------------------------------------------------
def test_toll_for_fastag_two_axle_gets_ten_percent_off():
    assert toll_for(2, False, True) == 90.0          # 100 * 0.9


@pytest.mark.parametrize("axles, expected", [
    (3, 142.5),   # 150 * 0.95
    (4, 237.5),   # 250 * 0.95
    (6, 380.0),   # 400 * 0.95
])
def test_toll_for_fastag_multi_axle_gets_five_percent_off(axles, expected):
    assert toll_for(axles, False, True) == expected


def test_toll_for_peak_and_fastag_combined_two_axle():
    assert toll_for(2, True, True) == 112.5          # 100 * 1.25 * 0.9


def test_toll_for_peak_and_fastag_combined_four_axle_is_rounded():
    # 250 * 1.25 * 0.95 = 296.875 -> rounded to 2 decimals
    assert toll_for(4, True, True) == round(296.875, 2)


def test_toll_for_result_has_at_most_two_decimals():
    result = toll_for(4, True, True)
    assert result == round(result, 2)


# ---------------------------------------------------------------------------
# toll_charge  (branch: vehicle in EXEMPT -> True / False)
# ---------------------------------------------------------------------------
def test_fire_engine_is_exempt():
    assert toll_charge("fire_engine", 6, True, False) == 0


def test_exempt_vehicle_skips_axle_validation():
    # Exempt vehicles return before toll_for is called, so a bad axle count is ignored
    assert toll_charge("ambulance", 0, True, True) == 0


@pytest.mark.parametrize("vehicle, axles, peak, tag, expected", [
    ("car", 2, False, False, 100),
    ("bus", 3, True, False, 187.5),
    ("truck", 4, False, True, 237.5),
    ("trailer", 7, True, True, 475.0),   # 400 * 1.25 * 0.95
])
def test_toll_charge_non_exempt_vehicles(vehicle, axles, peak, tag, expected):
    assert toll_charge(vehicle, axles, peak, tag) == expected


def test_toll_charge_non_exempt_invalid_axles_raises():
    with pytest.raises(ValueError):
        toll_charge("car", 1, False, False)


def test_exemption_is_case_sensitive():
    # "Ambulance" is not in EXEMPT, so it is charged like any other vehicle
    assert toll_charge("Ambulance", 2, False, False) == 100


# ---------------------------------------------------------------------------
# pass_advice  (loop 0 / many iterations; cost > / == / < pass_price)
# ---------------------------------------------------------------------------
def test_pass_advice_buy_pass_when_trips_cost_more():
    trips = [(False, False)] * 5                     # 5 * 100 = 500
    assert pass_advice(trips, 2, 450) == "buy_pass"


def test_pass_advice_either_when_cost_equals_price():
    trips = [(False, False)] * 3                     # 3 * 100 = 300
    assert pass_advice(trips, 2, 300) == "either"


def test_pass_advice_pay_per_trip_when_cheaper():
    trips = [(False, True), (True, False)]           # 90 + 125 = 215
    assert pass_advice(trips, 2, 500) == "pay_per_trip"


def test_pass_advice_no_trips():
    # Loop body never runs -> cost stays 0
    assert pass_advice([], 3, 0) == "either"
    assert pass_advice([], 3, 100) == "pay_per_trip"


def test_pass_advice_mixed_trips_heavy_vehicle():
    trips = [(True, True), (False, False), (True, False)]   # 475 + 400 + 500 = 1375
    assert pass_advice(trips, 6, 1000) == "buy_pass"


def test_pass_advice_invalid_axles_raises():
    with pytest.raises(ValueError):
        pass_advice([(False, False)], 1, 100)
