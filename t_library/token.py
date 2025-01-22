import argparse
import configparser

def handle_token_in_config():
    # Set up argparse for command-line argument parsing
    parser = argparse.ArgumentParser(description="Manage the SLACK token in the config file.")
    parser.add_argument(
        "--set-token",
        type=str,
        help="Set a new token value in the SLACK section of the configuration file.",
    )
    parser.add_argument(
        "--delete-token",
        action="store_true",
        help="Clear the value of the token field in the SLACK section of the configuration file.",
    )
    args = parser.parse_args()

    config = configparser.ConfigParser()
    config.read('./configurations/conf.ini')  # Load the existing config file

    # If --set-token is used
    if args.set_token:
        if not config.has_section('SLACK'):
            config.add_section('SLACK')  # Create the SLACK section if it doesn't exist
        config.set('SLACK', 'token', args.set_token)  # Set the token value
        with open('./configurations/conf.ini', 'w') as config_file:
            config.write(config_file)  # Write the changes back to the file
        print("Token value has been successfully updated in the configuration file.")

    # If --delete-token is used
    elif args.delete_token:
        if config.has_section('SLACK') and config.has_option('SLACK', 'token'):
            config.set('SLACK', 'token', '')  # Clear the token's value while keeping the key
            with open('./configurations/conf.ini', 'w') as config_file:
                config.write(config_file)  # Write the changes back to the file
            print("Token value has been successfully cleared.")
        else:
            print("Token value not found in the configuration file.")
    else:
        print("Please provide either --set-token or --delete-token.")

# Call the function
if __name__ == "__main__":
    handle_token_in_config()
