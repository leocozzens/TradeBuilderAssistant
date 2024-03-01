# External imports
from copy                    import deepcopy
import json
# Local imports
from modules.utils           import gen_map

class Portion(float):
    PORTION_MAX = 1.0
    def __new__(cls, raw):
        return super().__new__(cls, cls.verify_input(raw))

    @classmethod
    def verify_input(cls, raw):
        if not isinstance(raw, (int, float)):
            try:
                raw = float(raw)
            except:
                raise TypeError("Portion size must be a number")
        raw = abs(raw)
        if(raw > cls.PORTION_MAX):
            raise ValueError(f"Portion size must be less than or equal to {cls.PORTION_MAX:.1f}")
        return raw

DEFAULT_CONFIG = {
    "LIQUIDITY_FRACTION": Portion(0.50),
    "TARGETS":  { Portion(0.80): Portion(0.80), Portion(1.00): Portion(0.20) },
    "ACTIVATION_PORTION": Portion(0.33),
    "15":   { "ENTRY_BUFFER":  Portion(0.02), "SL_BUFFER": Portion(0.02) },
    "hour": { "ENTRY_BUFFER":  Portion(0.02), "SL_BUFFER": Portion(0.10) },
    "day":  { "ENTRY_BUFFER":  Portion(0.04), "SL_BUFFER": Portion(0.10) }
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