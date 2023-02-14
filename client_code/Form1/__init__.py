from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import plotly.graph_objects as go

class Form1(Form1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

        #Variables drop down menues:
        avg_power = [20, 30, 40, 60, 75, 100, 125, 135, 150, 175, 200]
        avg_power_str = [str(item) for item in avg_power]
        self.dd_avg_power.items = avg_power_str
        # print(avg_power_str)
        # print(f'Average power\n{avg_power}\n')
        
        run_time = [ item for item in range(1, 24+1) ]
        run_time_str = [str(item) for item in run_time]
        self.dd_run_time.items = run_time_str
        # print(f'Run time\n{run_time}\n')
        
        days_year = [ item for item in range(1, 365+1)]
        days_year_str = [str(item) for item in days_year]
        self.dd_days_year.items = days_year_str
        # print(f'Days of the year operating\n{days_year}\n')
        
        
        solar_irrad = [1.5, 2.6, 3, 4, 5.5, 6]
        solar_irrad_str = [str(item) for item in solar_irrad]
        self.dd_solar_irrad.items = solar_irrad_str
        # Solar radiation can be categorized into four classes: levels less than 2.6 kWh/m2 
        # are classified as low solar radiation while solar irradiance between 2.6-3 kWh/m2 
        # is moderate solar radiation; irradiance of between 3-4 kWh/m2 is high solar radiation
        # and irradiance higher than 4 kWh/m2 is very high radiation.
        # print(f'Average solar irradiation\n{solar_irrad}\n')
        
        wind_speed = [item for item in range(2, 15+1)]
        wind_speed_str = [str(item) for item in wind_speed]
        self.dd_wind_speed.items = wind_speed_str
        # print(f'Average wind speed\n{wind_speed}\n')
        
        fuel_cost = [1 + (item/10) for item in range(1, 11) ]
        fuel_cost_str = [str(item) for item in fuel_cost]
        self.dd_fuel_cost.items = fuel_cost_str
        # print(f'Average fuel cost\n{fuel_cost}\n')
        
        elect_grid_cost = [round((3 + (item/10))/10, 2) for item in range(4, 70)]
        elect_grid_cost_str = [str(item) for item in elect_grid_cost]
        self.dd_elect_grid_cost.items = elect_grid_cost_str
        # print(f'Electric grid cost\n{elect_grid_cost}\n')

        energy_inflation = [ item for item in range(10, 101, 10)]
        energy_inflation_str = [str(item) for item in energy_inflation]
        self.dd_energy_inflation.items = energy_inflation_str
        # print(f'Energy inflation\n{energy_inflation}\n')
        

    def run_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        #Selected values:
        
        avg_power_selected = anvil.server.call('str_to_num', self.dd_avg_power.selected_value)
        run_time_selected = anvil.server.call('str_to_num',self.dd_run_time.selected_value)
        days_year_selected = anvil.server.call('str_to_num',self.dd_days_year.selected_value)
        solar_irrad_selected = anvil.server.call('str_to_num',self.dd_solar_irrad.selected_value)
        wind_speed_selected = anvil.server.call('str_to_num',self.dd_wind_speed.selected_value)
        fuel_cost_selected = anvil.server.call('str_to_num',self.dd_fuel_cost.selected_value)
        elect_grid_cost_selected = anvil.server.call('str_to_num',self.dd_elect_grid_cost.selected_value)
        energy_inflation_selected = anvil.server.call('str_to_num',self.dd_energy_inflation.selected_value)

        #Outputs

        total_power_comsumption = avg_power_selected*run_time_selected*days_year_selected
        print(f'Total power comsumption: {total_power_comsumption} kWh')

        
        
        
        
        
       
        
       

        
        pass


    
        
  




