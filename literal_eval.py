import ast

# Load the content of the config file as a string
with open("config.py", "r") as file:
    config_content = file.read()

# Extract the dictionary part using literal_eval
config_dict = ast.literal_eval(config_content.split('=', 1)[1].strip())

# Now you can access the configuration dictionary
print(config_dict)
print("Database host:", config_dict["database"]["host"])
print("Logging enabled:", config_dict["features"]["enable_logging"])