# Local imports
import modules.input_handler as handler
from modules.config          import ConfigHandler
from modules.utils           import check_all, load_config

# Constants
VERSION = "0.9.4"

DEFAULT_LOCATION = "app/builder.conf"

LOGIN_MSG = "NOTE: ALL SETUPS ARE PROCESSED AS STOP-LIMIT ENTRIES; LIMIT ENTRIES AND CORRESPONDING TRADE CRITERIA WILL BE ADDED IN FUTURE UPDATE."
USAGE_MSG = "Enter a command (or type 'help' for more information)"
EXIT_MSG = "Thank you for using the Trade Builder"

# Main func
def main():
    print(LOGIN_MSG + "\n" + USAGE_MSG)

    while True:
        loadConf = input(f"\nWould you like to load the local config - {DEFAULT_LOCATION.split('/')[-1]}? (Y/N) ")
        if check_all(loadConf.lower(), ["n", "no"]) or check_all(loadConf.lower(), ["y", "yes"]):
            break
        print(f"Error: '{loadConf}' is not a valid response. Please specify 'yes' or 'no'")

    if check_all(loadConf.lower(), [ "y", "yes" ]):
        status, result = load_config(DEFAULT_LOCATION)
        if(status):
            print(f"\nConfig loaded successfuly; {result}")
        else:
            print(f"\nError loading config; {result}\nDefaulting to standard config")
        print(ConfigHandler.current_profile_info())

    print("")
    active = True
    while active:
        active = handler.cycle_input(VERSION)
    print(f"\n{EXIT_MSG} - {VERSION}")

# Init idiom
if __name__ == '__main__':
    main()