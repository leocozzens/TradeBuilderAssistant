# External imports
from math import ceil, floor

def roundup(value: float, digit: int) -> float:
    multiplier = 10 ** digit
    return ceil(value * multiplier) / multiplier

def rounddown(value: float, digit: int) -> float:
    multiplier = 10 ** digit
    return floor(value * multiplier) / multiplier

def roundreg(value: float, digit: int) -> float:
    multiplier = 10 ** digit
    return round(value * multiplier) / multiplier

def calc_activation(entry: float, zoneSize: float, activationRule: float) -> float:
    return entry + zoneSize * activationRule

def stop_buff(zones: int, dailyATR: float):
    targets = zones + 1
    targetPrices = []

    stopLossBuffer = roundup(dailyATR, 2)