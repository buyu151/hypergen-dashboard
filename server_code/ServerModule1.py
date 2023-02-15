import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
from Form1 import Form1

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#

@anvil.server.callable
def str_to_num(val):
        if val.isdigit():
            num_val = int(val)
        else:
            num_val = float(val)
        return num_val

@anvil.server.callable
def create_df(l1, l2):
    df = df = pd.DataFrame(l1,l2)
    print(df.head())
    return df
    


