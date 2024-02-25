# External imports
from copy   import copy, deepcopy
import json

class ZoneSpec:
    def __init__(self, lowest: float, zoneSet: dict | None):
        self.lowestFract = lowest
        self.zoneSet = zoneSet
        if(zoneSet == None): self.sizes = None
        else: self.sizes = list(zoneSet.keys()).sort()

    def get_activation(self, szSize: float, entry: float) -> float:
        activation = ZoneSpec.calc_activation(entry, szSize, self.lowestFract)
        if(self.sizes == None):
            return activation
        for i in self.sizes:
            if szSize > i:
                return activation
            activation = ZoneSpec.calc_activation(entry, szSize, self.zoneSet[i])
        return activation

    @staticmethod
    def calc_activation(entry: float, szSize: float, fract: float) -> float:
        return entry + szSize / fract

DEFAULT_CONFIG = {
    "LIQUIDITY_FRACTION": 0.50,
    "TARGETS":  { 0.80: 0.80, 1.00: 0.20 },
    "ZONE_SPEC": ZoneSpec(5, { 0.5: 4, 1.0: 3 }),
    "15":   { "ENTRY_BUFFER":  0.02, "SL_BUFFER": 0.02 },
    "hour": { "ENTRY_BUFFER":  0.02, "SL_BUFFER": 0.10 },
    "day":  { "ENTRY_BUFFER":  0.04, "SL_BUFFER": 0.10 }
}

class ConfigHandler:
    currentConfig: dict = deepcopy(DEFAULT_CONFIG)
    @classmethod
    def fetch(cls, path: str) -> bool | list:
        try:
            with open(path) as f:
                data = json.load(f)
        except Exception as e:
            return False, e
        if(type(data) != dict):
            return False, "Improper configuration formatting"
        cls.loadtoconfig(cls.currentConfig, data)
        return True

    @classmethod
    def loadtoconfig(cls, config: dict, new: dict):
        configKeys = list(config.keys())
        newKeys = {}
        for i in list(new.keys()):
            found = False
            for j in configKeys:
                if type(j)(i) == j:
                    newKeys[j] = i
                    found = True
                    break
            if not found:
                print(f"Could not find key value {i} in config")

        for i in list(newKeys.keys()):
            if(type(new[newKeys[i]]) == dict):
                cls.loadtoconfig(config[i], new[newKeys[i]])
            else:
                try:
                    config[i] = type(config[i])(new[newKeys[i]])
                    print(f"Value of {i} is {config[i]}")
                except:
                    print(f"Unable to set {i}, incompatible value")
                
    @classmethod
    def reset(cls):
        cls.currentConfig = deepcopy(DEFAULT_CONFIG)

    @staticmethod
    def converttotype(data: list, t: type) -> list:
        for i in range(0, len(data)):
            try:
                data[i] = t(data[i])
            except:
                continue
        return data