import os

base_dir = os.getcwd()

configurations = ["username",  "password",
                  "base_dir",  "server_address", "TRANS_LIMIT", "image_url", "audio_url", "video_url"]
values = ["", "", base_dir, "http://127.0.0.1:8000",  "5", "/api/create", "", "/api/createVideo"]
config_dict = {}


def create_config(editing):
    index = 0
    for configuration in configurations:
        print(f"\n{configuration}")
        if values[index]:
            if editing:
                print(f" Current value : {values[index]} ")
                value = str(
                    input("Enter new value (or press enter to keep current value): "))
            else:
                print(f" Default : {values[index]} ")
                value = str(
                    input("Enter value (or press enter to keep default): "))

            value = value.replace("\"", "\\\"")
            if value:
                config_dict[configuration] = value
            else:

                config_dict[configuration] = values[index]

        else:
            value = input(f"Enter value: ")
            config_dict[configuration] = value
        index += 1


def save_config(config_dict):
    lines = ["# This is an auto-generated file\n",
             "# You can edit these configurations directly or by running the setup.py script\n"
             "# Note that errors in the config file can result into the failure of the whole client\n"
             "# So be careful while editing, thanks \n\n"]
    for key in config_dict:
        if(config_dict[key].isdigit()):
            lines.append(f"{key} = {config_dict[key]}\n")
        else:
            lines.append(f"{key} = \"{config_dict[key]}\"\n")

    # Now save the configurations
    with open("config.py", "w+") as f:
        f.write("# client configurations\n\n")
        f.close()

    with open("config.py", "a+") as f:
        f.writelines(lines)


def load_config():
    with open("config.py",  "r+") as f:
        for line in f:
            if (not line) or line.find("#") != -1 or line.find("=") == -1:  # skip comments
                continue
            name, value = line.split('=')
            name = name.strip()
            value = value.strip().strip("\"")
            values[configurations.index(name)] = value
        f.close()
        return


if __name__ == "__main__":
    if os.path.isfile("config.py"):
        choice = input(
            "There are some configurations already. Do you want to edit them? (yes/no):")
        if choice[0].lower() == 'y':
            load_config()
            create_config(True)
        else:
            print("Exiting...")
            exit(0)
    else:
        print("No config file found, Let's create one")
    create_config(False)

    save_config(config_dict)

    print("\nConfiguration saved successfully")
    print("You can now run the client")
    print("\nTo run the client, run the following command:")
    print("python3 client.py \n Enjoy!")
