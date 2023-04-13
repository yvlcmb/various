#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Mobility module for calculating mobility and vehicle cone indices"""
from typing import NamedTuple, Callable


class Vehicle(NamedTuple): 
    category: str  # both
    hydraulic: bool = True # both
    grouser_ht: float = 0 # both
    clearance: int = 0  # both
    hp: int = 0  # both
    weight: int = 0  # both 
    axles: int = 0  # wheeled
    chains: bool = False
    tires: int = 0  # wheeled
    tire_diameter: int = 0 # wheeled
    tire_width: int = 0  # wheeled
    wheels: int = 0  # wheeled
    bogies: int = 0  # tracked
    length: int = 0  # tracked 
    shoe_area: int = 0  # tracked
    track_width: int = 0  # tracked


def factor_weight(veh: Vehicle) -> Callable: 
    """Calculate the weight factor"""
    def _wheel(): 
        lbs_per_axle = veh.weight / veh.axles
        cons = (
        (2_000, 0.533, 0),
        (13_500, 0.033, 1.05),
        (20_000, 0.142, -0.42),
        (100_000, 0.278, -3.115))
        mod, val = next(filter(lambda x: x[0] >= lbs_per_axle, cons))[1:]
        return mod * ((veh.weight/1000) / veh.axles) + val
    def _track(): 
        cons = (
            (50_000, 1.0), 
            (70_000, 1.2), 
            (100_000, 1.4), 
            (1_000_000, 1.8))
        return next(filter(lambda x: x[0] >= veh.weight, cons))[1]
    return (_wheel, _track)[veh.category == 'track']


def factor_pressure(veh: Vehicle) -> Callable: 
    """Calculate the ground contact pressure factor"""
    def _wheel(): 
        return veh.weight / ((veh.tire_width * veh.tires * (veh.tire_diameter / 2)))
    def _track(): 
        return veh.weight / (veh.length * veh.track_width)
    return (_wheel, _track)[veh.category == 'track']


def factor_tire_track(veh: Vehicle) -> Callable:
    """Calculate the track or tire factor"""
    def _tire():
        return (veh.tire_width + 10) / 100
    def _track(): 
        return veh.track_width / 100
    return (_tire, _track)[veh.category == 'track']


def factor_transmission(veh: Vehicle) -> float: 
    return (1.0, 1.05)[veh.hydraulic]


def factor_grouser(veh: Vehicle) -> float: 
    """Calculate the grouser factor"""
    def _wheel():
        return (1.0, 1.5)[veh.chains]
    def _track(): 
        return (1.0, 1.1)[veh.grouser_ht > 1.5]
    return (_wheel, _track)[veh.category == 'track']


def factor_clearance(veh: Vehicle) -> float: 
    return veh.clearance /10


def factor_engine(veh: Vehicle) -> float:
    """Calculate the engine factor"""
    hp_per_ton = veh.hp / (veh.weight / 2000)
    return (1.05, 1.0)[hp_per_ton <= 10]


def factor_bogie_wheel(veh: Vehicle) -> Callable:
    """Calculate the bogie or wheel factors"""
    def _bogie():
        return (veh.weight / 10) / (veh.bogies * veh.shoe_area)
    def _wheel_load(): 
        return (veh.weight / 1000) / veh.wheels
    return (_wheel_load, _bogie)[veh.category == 'track']


def calculate_mobility(veh): 
    """Calculate the Revised Mobility Index for wheeled and tracked vehicles"""
    engine = factor_engine(veh)
    clear = factor_clearance(veh)
    trans = factor_transmission(veh)
    tire_track = factor_tire_track(veh)
    grouser = factor_grouser(veh)
    press = factor_pressure(veh)
    weight = factor_weight(veh)
    bogie = factor_bogie_wheel(veh)
    product1 = press() * weight()
    product2 = tire_track() * grouser()
    return ((product1 / product 2) + bogie() - clear) * engine * trans



def test_mobility_tracked(): 
    veh = Vehicle(**abrams)
    engine = factor_engine(veh)
    clear = factor_clearance(veh)
    trans = factor_transmission(veh)
    tire_track = factor_tire_track(veh)()
    grouser = factor_grouser(veh)
    press = round(factor_pressure(veh)(), 3)
    weight = factor_weight(veh)()
    bogie = round(factor_bogie_wheel(veh)(), 3)
    actual = (engine, clear, trans, tire_track, grouser, press, weight, bogie)
    expected = (1.05, 1.9, 1.05, 0.25, 1, 14.129, 1.8, 10.225)
    assert actual == expected


if __name__ == "__main__":
    abrams = {
        'length': 385,
        'weight': 136000,
        'track_width': 25,
        'shoe_area': 190,
        'hydraulic': True,
        'bogies': 7,
        'hp': 1500,
        'clearance': 19,
        'category': 'track'}

    stryker = {
        'category': 'wheel',
        'weight': 36320,
        'axles': 4,
        'clearance': 21,
        'wheels': 8,
        'tire_width': 14.5,
        'hydraulic': True,
        'tire_diameter': 45,
        'tires': 8,
        'hp': 350}

    mbt = Vehicle(**abrams)
    ifv = Vehicle(**stryker)
    assert round(calculate_mobility(ifv)) == 87
    assert round(calculate_mobility(mbt)) == 121
    test_mobility_tracked()
