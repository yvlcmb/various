#!/usr/bin/python3
# -*- coding: utf-8 -*-

from typing import NamedTuple, Callable


class Vehicle(NamedTuple): 
    category: str  # both
    hydraulic: bool = True # both
    clearance: int = 0  # both
    hp: int = 0  # both
    weight: int = 0  # both 
    axles: int = 0  # wheeled
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


if __name__ == "__main__"::
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
        'tire_width': 22,
        'hydraulic': True,
        'tire_diameter': 45,
        'tires': 8,
        'hp': 350}
    
    veh = Vehicle(**abrams)
    print(factor_weight(veh)())
