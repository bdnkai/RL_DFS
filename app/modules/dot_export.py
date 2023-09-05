import os
from dotenv import load_dotenv as ld_env


def secrets(path_to_env):
    ld_env(path_to_env)

    entry_point = os.getenv("SECRET_PATH")
    data_point_one = os.getenv("SECRET_A")
    data_point_two = os.getenv("SECRET_B")
    data_pont_three = os.getenv("SECRET_C")
    data_pont_four = os.getenv("SECRET_D")
    access_point = os.getenv("SECRET_KEY")

    secret_vars = entry_point, data_point_one, data_point_two, data_pont_three, data_pont_four, access_point

    return secret_vars
