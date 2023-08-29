import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
import uuid

# ---------------------------------------------------------------------------------------------------

# See this sites for help on pandas on anvil:
# https://anvil.works/forum/t/using-pandas-with-anvil/1699/2
# https://anvil.works/learn/tutorials/web-app-with-pandas

# ---------------------------------------------------------------------------------------------------

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

#---------------------------------------------------------------------------------------------------------
#Server callable functions

#convert strings to numbers
@anvil.server.callable
def str_to_num(val):
        if val.isdigit():
            num_val = int(val)
        else:
            num_val = float(val)
        return num_val

#convert lists to pandas dataframe
@anvil.server.callable
def create_df(l1, l2):
    df = pd.DataFrame(l1,l2)
    print(df.head())
    return df
    
#Import user inputs for data analysis
@anvil.server.callable
def add_inputs(avg_power_selected, run_time_selected, days_year_selected, solar_irrad_selected, wind_speed_selected, fuel_cost_selected, elect_grid_cost_selected, energy_inflation_selected, session_time, run_press ):
  app_tables.user_inputs.add_row(
    avg_power_selected=avg_power_selected, 
    run_time_selected=run_time_selected, 
    days_year_selected=days_year_selected,
    solar_irrad_selected=solar_irrad_selected,
    wind_speed_selected=wind_speed_selected,
    fuel_cost_selected=fuel_cost_selected,
    elect_grid_cost_selected=elect_grid_cost_selected,
    energy_inflation_selected=energy_inflation_selected,
    created=session_time,
    run_press = run_press  
  )

#calculate total power requirement and save it to results table
@anvil.server.callable
def clac_total_power(avg_power_selected, run_time_selected, days_year_selected):
    total_power_comsumption = avg_power_selected*run_time_selected*days_year_selected
    return total_power_comsumption

@anvil.server.callable
def add_total_power(total_power, session_time, run_press):
    app_tables.total_power.add_row(
        power_comsumption=total_power,
        created=session_time,
        run_press = run_press
    )
                                   
#Import capital costs to server
@anvil.server.callable
def add_capital_costs(piston_capital, piston_fuel, piston_maintenance, mgt_capital, mgt_fuel, mgt_maintenance, hmgt_capital, hmgt_fuel, hmgt_maintenance, solar_capital, solar_maintenance, wind_capital, wind_maintenance, session_time, run_press ):
  app_tables.capital_costs_yearly.add_row(
      piston_capital=piston_capital,
      piston_fuel=piston_fuel,
      piston_maintenance=piston_maintenance,
      mgt_capital=mgt_capital,
      mgt_fuel=mgt_fuel,
      mgt_maintenance=mgt_maintenance, 
      hmgt_capital=hmgt_capital, 
      hmgt_fuel=hmgt_fuel,
      hmgt_maintenance=hmgt_maintenance,
      solar_capital=solar_capital,
      solar_maintenance=solar_maintenance,
      wind_capital=wind_capital,
      wind_maintenance=wind_maintenance,   
     created=session_time,
     run_press = run_press
  )

@anvil.server.callable
def add_cumulative_costs(year, piston, mgt, hmgt, solar, wind, grid, session_time, run_press):
    app_tables.cumulative_costs.add_row(year=year,
                                        piston=piston,
                                        mgt=mgt,
                                        hmgt=hmgt,
                                        solar=solar,
                                        wind=wind,
                                        grid=grid,
                                        created=session_time,
                                        run_press = run_press
                                       )


    
#Get user id for session 
#https://anvil.works/forum/t/how-do-you-define-a-session/606
@anvil.server.callable
def get_uuid():
  if "id" not in anvil.server.session:
    anvil.server.session['id']=str(uuid.uuid4())

  return anvil.server.session['id']

#Create an iterable object with the cumulative cost table ----------------------------------------------------
# @anvil.server.callable
def cumulative_cost_df():
    cumulative_costs = app_tables.cumulative_costs.search()
    dicts = [{'year': r['year'], 'piston': r['piston'], 'mgt': r['mgt'], 'hmgt': r['hmgt'], 'solar': r['solar'], 'wind': r['wind'], 'grid': r['grid'],}
         for r in cumulative_costs]
    df = pd.DataFrame.from_dict(dicts)
    return df
    
@anvil.server.callable
def explore():
  cc_df = cumulative_cost_df()
  # print(cc_df.head())
  # print(cc_df.tail())
  print(cc_df)

# Making plots----------------------------------------------------------------------------------------------

# https://plotly.com/python/subplots/
# https://plotly.com/python/line-and-scatter/
# https://stackoverflow.com/questions/67381580/how-to-add-two-line-in-the-same-canvas-in-plotly
# https://plotly.com/python/line-charts/

@anvil.server.callable
def create_plots():
    cc_df = cumulative_cost_df()
    fig = px.line(cc_df, x= 'year', y= ['piston', 'mgt', 'hmgt', 'solar', 'wind', 'grid'], text="year", title='Cumulative cost')
    fig.update_traces(textposition="bottom right")
   
    return fig



#------------------------------------------------------------------------------------------------------------------
#delete cumulative cost table after each session https://anvil.works/docs/api/anvil.tables
@anvil.server.callable
def delete_cumulative_costs():
    app_tables.cumulative_costs.delete_all_rows()





    
    
