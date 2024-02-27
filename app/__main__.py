# Local imports
import modules.input_handler as handler
from modules.config          import ConfigHandler
from modules.utils           import gen_map
from modules.input_handler   import check_all

# Constants
VERSION = "0.9.1"

DEFAULT_LOCATION = "app/builder.conf"

LOGIN_MSG = "NOTE: ALL SETUPS ARE PROCESSED AS STOP-LIMIT ENTRIES; LIMIT ENTRIES AND CORRESPONDING TRADE CRITERIA WILL BE ADDED IN FUTURE UPDATE."
USAGE_MSG = "Enter a command (or type 'help' for more information)"
EXIT_MSG = "Thank you for using the Trade Builder"

# def stringize_list(data, fmt)

def load_config(path: str) -> bool | str:
    error, failed = ConfigHandler.fetch(path)
    if error != "":
        return False, error

    failedList = list(failed.keys())
    if len(failedList) < 1:
        return True, "All configuration values set successfully"

    fmt = "{} - {}"
    failedStr = fmt.format(failedList[0], failed[failedList[0]])
    for i in range(1, len(failedList)):
        failedStr += f", " + fmt.format(failedList[i], failed[failedList[i]])

    return True, f"The following failed: {failedStr}"


# Main func
def main():
    print(LOGIN_MSG + "\n" + USAGE_MSG)

    if check_all(input(f"\nWould you like to load the local config - {DEFAULT_LOCATION.split('/')[-1]}? (Y/N) "), [ "y", "yes" ]):
        success, result = load_config(DEFAULT_LOCATION)
        if(success):
            print(f"\nConfig loaded successfuly; {result}")
        else:
            print(f"\nError loading config; {result}\nDefaulting to standard config")
        print(f"Using config profile: {ConfigHandler.get_profile_name()}\n{gen_map(ConfigHandler.get_current_profile())}")

    active = True
    while active:
        active = handler.cycle_input(VERSION)
    print(f"\n{EXIT_MSG} - {VERSION}")

# Init idiom
if __name__ == '__main__':
    main()