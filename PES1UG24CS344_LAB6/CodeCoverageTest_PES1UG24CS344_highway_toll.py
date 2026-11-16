"""Code (line/statement) coverage tests for highway_toll.py
Priyansh Soni - PES1UG24CS344

Goal: execute every line of highway_toll.py at least once (>= 90% line coverage)
with the smallest useful set of tests - one test per previously unexecuted line.
BranchCoverageTest_PES1UG24CS344_highway_toll.py then tests every decision outcome
(True and False) separately, plus boundary and edge cases.
"""
import pytest
from highway_toll import toll_for, toll_charge, pass_advice


# Given example tests
def test_ambulance_is_exempt():
    assert toll_charge("ambulance", 2, False, False) == 0


def test_two_axle_base_toll():
    assert toll_for(2, False, False) == 100


# Line: raise ValueError("invalid axle count")
def test_invalid_axle_count_raises():
    with pytest.raises(ValueError):
        toll_for(1, True, True)


# Lines: base = 400 (axle count not in BASE_TOLL), peak surcharge, 5% FASTag discount
def test_heavy_vehicle_peak_with_fastag():
    assert toll_for(6, True, True) == 475.0          # 400 * 1.25 * 0.95


# Lines: base = BASE_TOLL[...], peak surcharge, 10% FASTag discount for 2 axles
def test_car_peak_with_fastag():
    assert toll_for(2, True, True) == 112.5          # 100 * 1.25 * 0.9


# Line: return toll_for(...) inside toll_charge (non-exempt vehicle)
def test_non_exempt_vehicle_is_charged():
    assert toll_charge("truck", 3, True, True) == 178.12   # 150 * 1.25 * 0.95 = 178.125


# Line: return "buy_pass"
def test_pass_advice_buy_pass():
    assert pass_advice([(True, True)] * 3, 2, 300) == "buy_pass"     # 3 * 112.5 = 337.5


# Line: return "either"
def test_pass_advice_either():
    assert pass_advice([(True, True)] * 2, 2, 225) == "either"       # 2 * 112.5 = 225


# Line: return "pay_per_trip"
def test_pass_advice_pay_per_trip():
    assert pass_advice([(True, True)], 2, 500) == "pay_per_trip"
