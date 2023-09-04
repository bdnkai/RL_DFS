import os
import sys
from dotenv import load_dotenv as ld_dot

sys.path.append('/x/personal_project/bdn_portfolio/rl_dfs/')


ld_dot('../../.env')
def get_env(variable):
    return os.getenv(variable)


dot_var = url, login_url, spider_script

print(dot_var)