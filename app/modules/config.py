# External imports
from copy                    import deepcopy
import json
# Local imports
from modules.utils           import gen_map

class ZoneSpec:
    def __init__(self, lowest: float, zoneSet: dict | None):
        self.lowestFract = lowest
        self.zoneSet = zoneSet
        if(zoneSet == None): self.sizes = None
        else: self.sizes = list(zoneSet.keys()).sort()

    def __repr__(self) -> str:
        return "Test" #TODO: Modify this temp value

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
    profileName: str = "Default"

    @classmethod
    def fetch(cls, path: str) -> str | dict:
        path = path.replace('\\', '/')
        try:
            with open(path) as f:
                data = json.load(f)
        except Exception as e:
            return str(e) if str(e) != "" else f"Could not load data from {path}", {}
        if(type(data) != dict):
            return "Improper configuration formatting", {}
        return "", data

    @classmethod
    def set_config(cls, name: str, new: dict) -> dict:
        ConfigHandler.reset()
        ConfigHandler.set_profile_name(name)
        return ConfigHandler.load_to_config(cls.currentConfig, new)

    # Expects new key values to be strings, as json only supports strings as key values
    @classmethod
    def load_to_config(cls, config: dict, new: dict) -> dict:
        failed: dict = {}
        configKeys = list(config.keys())

        newKeys = {}
        for i in list(new.keys()):
            found: bool = False
            for j in configKeys:
                try:
                    if type(j)(i) == j:
                        newKeys[j] = i
                        found = True
                        break
                except:
                    continue
            if not found:
                failed[i] = "Could not find key value"
                print(type(i))

        for i in list(newKeys.keys()):
            if(type(new[newKeys[i]]) == dict):
                subFailed = cls.load_to_config(config[i], new[newKeys[i]])
                for j in list(subFailed.keys()):
                    subFailed[newKeys[i] + " " + j] = subFailed[j]
                    del subFailed[j]
                failed = { **failed, **subFailed }
            else:
                try:
                    config[i] = type(config[i])(new[newKeys[i]])
                except Exception as e:
                    failed[newKeys[i]] = f"Unable to set value: {str(e)}"

        return failed

    @classmethod
    def reset(cls):
        cls.currentConfig = deepcopy(DEFAULT_CONFIG)
        cls.profileName = "Default"

    @classmethod
    def set_profile_name(cls, name: str):
        cls.profileName = name

    @classmethod
    def current_profile_info(cls) -> str:
       return  f"Using config profile: {ConfigHandler.get_profile_name()}\n{gen_map(ConfigHandler.get_current_profile())}"

    @classmethod
    def get_profile_name(cls) -> str:
        return cls.profileName

    @classmethod
    def get_current_profile(cls) -> dict:
        return cls.currentConfig

    @staticmethod
    def get_name_from_path(path: str):
        return path.replace('\\', '/').split('/')[-1].split('.')[0]