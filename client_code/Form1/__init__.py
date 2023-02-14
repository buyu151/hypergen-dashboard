from ._anvil_designer import Form1Template
from anvil import *
import plotly.graph_objects as go

class Form1(Form1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

        #Variables:
        avg_power = [20, 30, 40, 60, 75, 100, 125, 135, 150, 175, 200]
        # print(f'Average power\n{avg_power}\n')
        
        run_time = [ item for item in range(1, 24+1) ]
        # print(f'Run time\n{run_time}\n')
        
        days_year = [ item for item in range(1, 365+1)]
        # print(f'Days of the year operating\n{days_year}\n')
        
        solar_irrad = [1.5, 2.6, 3, 4, 5.5, 6]
        # Solar radiation can be categorized into four classes: levels less than 2.6 kWh/m2 
        # are classified as low solar radiation while solar irradiance between 2.6-3 kWh/m2 
        # is moderate solar radiation; irradiance of between 3-4 kWh/m2 is high solar radiation
        # and irradiance higher than 4 kWh/m2 is very high radiation.
        # print(f'Average solar irradiation\n{solar_irrad}\n')
        
        wind_speed = [item for item in range(2, 15+1)]
        # print(f'Average wind speed\n{wind_speed}\n')
        
        fuel_cost = [1 + (item/10) for item in range(1, 11) ]
        # print(f'Average fuel cost\n{fuel_cost}\n')
        
        elect_grid_cost = [round((3 + (item/10))/10, 2) for item in range(4, 70)]
        # print(f'Electric grid cost\n{elect_grid_cost}\n')

        energy_inflation = [ item for item in range(10, 101, 10)]
        # print(f'Energy inflation\n{energy_inflation}\n')

    
        
        

    def text_box_1_pressed_enter(self, **event_args):
        """This method is called when the user presses Enter in this text box"""
        pass

    def drop_down_6_change(self, **event_args):
        """This method is called when an item is selected"""
        pass

    def drop_down_1_change(self, **event_args):
        """This method is called when an item is selected"""
        pass



