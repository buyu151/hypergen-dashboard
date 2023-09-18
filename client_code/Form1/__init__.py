from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import plotly.graph_objects as go
import time
from datetime import datetime
from random import randint


# https://anvil.works/learn/tutorials/web-app-with-pandas
class Form1(Form1Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.

        #-----------------------------------------------------------------------------------------------------------
        #Variables drop down menus:

        t_begin = time.time()
        
        self.avg_power = ['20', '30', '40', '60', '75', '100', '125', '135', '150', '175', '200']
        self.dd_avg_power.items = self.avg_power #dd for drop down menue
        self.dd_avg_power.selected_value = '30' #Default value in drop down menue
        # print(f'Average power\n{self.avg_power}\n')
        
        self.run_time = [ str(item) for item in range(1, 24+1) ]
        self.dd_run_time.items = self.run_time
        self.dd_run_time.selected_value = '8' #Default value
        # print(f'Run time\n{self.run_time}\n')
        
        self.days_year = [ str(item) for item in range(1, 365+1)]
        self.dd_days_year.items = self.days_year
        self.dd_days_year.selected_value = '250' #Default value
        # print(f'Days of the year operating\n{self.days_year}\n')
        
        
        self.solar_irrad = ['1.5', '2.6', '3', '4', '5.45', '6']
        self.dd_solar_irrad.items = self.solar_irrad
        self.dd_solar_irrad.selected_value = '5.45' #Default value
        # Solar radiation can be categorized into four classes: levels less than 2.6 kWh/m2 
        # are classified as low solar radiation while solar irradiance between 2.6-3 kWh/m2 
        # is moderate solar radiation; irradiance of between 3-4 kWh/m2 is high solar radiation
        # and irradiance higher than 4 kWh/m2 is very high radiation.
        # print(f'Average solar irradiation\n{self.solar_irrad}\n')
        
        self.wind_speed = [str(item) for item in range(2, 15+1)]
        self.dd_wind_speed.items = self.wind_speed
        self.dd_wind_speed.selected_value = '5' #Default value
        # print(f'Average wind speed\n{self.wind_speed}\n')
        
        self.fuel_cost = [str(1 + (item/10)) for item in range(0, 11) ]
        self.dd_fuel_cost.items = self.fuel_cost
        self.dd_fuel_cost.selected_value = '1.0' #Default value
        # print(f'Average fuel cost\n{self.fuel_cost}\n')
        
        self.elect_grid_cost = [str(round((3 + (item/10))/10, 2)) for item in range(4, 70)]
        self.dd_elect_grid_cost.items = self.elect_grid_cost
        self.dd_elect_grid_cost.selected_value = '0.34' #Default value
        # print(f'Electric grid cost\n{self.elect_grid_cost}\n')

        self.energy_inflation = [ str(item) for item in range(10, 101, 10)]
        self.dd_energy_inflation.items = self.energy_inflation
        self.dd_energy_inflation.selected_value = '30' #Default value
        # print(f'Energy inflation\n{self.energy_inflation}\n')

        t_end = time.time()
        print(f'Build drop down list values in {t_end-t_begin} seconds')
        

    def run_button_click(self, **event_args):      
        
        """This method is called when the button is clicked"""
        #-----------------------------------------------------------------------------------------------------------
        #Delete previous run
        anvil.server.call('delete_cumulative_costs')
        
        #-----------------------------------------------------------------------------------------------------------
        #Random number assigned to each play press to keep track of curren calculation
        
        self.run_num = randint(0, 1000000)
        # print(f"run press {self.run_num}")

        #-----------------------------------------------------------------------------------------------------------
        #Get user id
        self.user_id = anvil.server.call('get_uuid')
        print(f'User id is {self.user_id}')
        
        #-----------------------------------------------------------------------------------------------------------
        #Selected values copnverted to numbers:

        self.session_time = datetime.now()

        t_begin_total = time.time()

        t_begin = time.time()

            
        self.avg_power_selected = float(self.dd_avg_power.selected_value)
        self.run_time_selected = float(self.dd_run_time.selected_value)
        self.days_year_selected = float(self.dd_days_year.selected_value)
        self.solar_irrad_selected = float(self.dd_solar_irrad.selected_value)
        self.wind_speed_selected = float(self.dd_wind_speed.selected_value)
        self.fuel_cost_selected = float(self.dd_fuel_cost.selected_value)
        self.elect_grid_cost_selected = float(self.dd_elect_grid_cost.selected_value)
        self.energy_inflation_selected = float(self.dd_energy_inflation.selected_value)

        t_end = time.time()
        print(f'Done converting imputs to numbers in {t_end-t_begin} seconds')

        #-----------------------------------------------------------------------------------------------------------
        #Pass user options to the server 

        t_begin = time.time()

        anvil.server.call('add_inputs',
                          self.avg_power_selected,
                          self.run_time_selected,
                          self.days_year_selected,
                          self.solar_irrad_selected,
                          self.wind_speed_selected,
                          self.fuel_cost_selected,
                          self.elect_grid_cost_selected,
                          self.energy_inflation_selected,
                          self.session_time,
                          self.run_num,
                          self.user_id
                         )

        t_end = time.time()

        anvil.server.call('get_inputs',
                         self.avg_power_selected,
                          self.run_time_selected,
                          self.days_year_selected,
                          self.solar_irrad_selected,
                          self.wind_speed_selected,
                          self.fuel_cost_selected,
                          self.elect_grid_cost_selected,
                          self.energy_inflation_selected
                         )
        
        print(f'Done importing imputs to server in {t_end-t_begin} seconds')
        
        #-----------------------------------------------------------------------------------------------------------
        #Outputs

        t_begin = time.time()
        # self.total_power_comsumption = anvil.server.call('clac_total_power', self.avg_power_selected, self.run_time_selected, self.days_year_selected)
        self.total_power_comsumption = self.avg_power_selected*self.run_time_selected*self.days_year_selected
        t_end = time.time()
        print(f'Total power comsumption: {self.total_power_comsumption} kWh calculated in {t_end-t_begin} seconds')

        
        t_begin = time.time()
        anvil.server.call('add_total_power', self.total_power_comsumption, self.session_time, self.run_num, self.user_id)
        t_end = time.time()
        print(f'Done importing total power comsumption to server in {t_end-t_begin} seconds')
        

        #-----------------------------------------------------------------------------------------------------------
        #Generate capital costs dictionary for all power generators:
        t_begin = time.time()
        self.capital_costs = {}
        self.generators = ['piston', 'MGT', 'HMGT', 'solar', 'wind']
        self.cost_factor = {'piston': 0.15, 'MGT': 0.0045, 'HMGT': 0.0045, 'solar':3000, 'wind': 0.0082}

        #Get column names from app tables
        self.column_generator_costs = app_tables.generator_cost.list_columns()[1]['name'] #column 'pounds_per_kwh' in table 3
        self.column_generator_efficiency = [app_tables.generator_efficiency.list_columns()[i]['name'] for i in range(1, 4)] #efficiency columns 45, 35 and 50 in table 2
        # print(column_generator_efficiency)

        self.generator_efficiency_obj = app_tables.generator_efficiency.get(generator_size=self.avg_power_selected)
        # print(f'gen eff{generator_efficiency_obj}')

        for item in self.generators:
            #Object for table row 
            self.generator_cost_obj = app_tables.generator_cost.get(generator=item)
            self.capital_costs[item] = {'Initial capital cost': self.generator_cost_obj[self.column_generator_costs]*self.avg_power_selected}
            if item == 'solar':
                self.capital_costs[item]['Yearly maintenance costs'] = self.cost_factor['solar']
            else:
                self.capital_costs[item]['Yearly maintenance costs'] = self.total_power_comsumption*self.cost_factor[item]
                
            if item not in ['solar', 'wind']: 
                if item == 'piston':
                    self.efficiency = '45'
                elif item == 'MGT':
                    self.efficiency = '35'
                elif item == 'HMGT':
                    self.efficiency = '50'      
                self.fuel_data = app_tables.generator_efficiency.get(generator_size=self.avg_power_selected)[self.efficiency]
                # print(f'fuel data: {fuel_data}')
                self.capital_costs[item]['Yearly fuel costs'] = self.fuel_data*self.run_time_selected*self.days_year_selected*self.fuel_cost_selected 
        t_end = time.time()
        print(f'Capital costs calculated in {t_end-t_begin} seconds:\n')
        # print(self.capital_costs)

        #-----------------------------------------------------------------------------------------------------------
        #Import capital costs to server

        t_begin = time.time()

        anvil.server.call('add_capital_costs',
                          self.capital_costs['piston']['Initial capital cost'],
                          self.capital_costs['piston']['Yearly maintenance costs'],
                          self.capital_costs['piston']['Yearly fuel costs'],
                          self.capital_costs['MGT']['Initial capital cost'],
                          self.capital_costs['MGT']['Yearly maintenance costs'],
                          self.capital_costs['MGT']['Yearly fuel costs'],
                          self.capital_costs['HMGT']['Initial capital cost'],
                          self.capital_costs['HMGT']['Yearly maintenance costs'],
                          self.capital_costs['HMGT']['Yearly fuel costs'],
                          self.capital_costs['solar']['Initial capital cost'],
                          self.capital_costs['solar']['Yearly maintenance costs'],
                          self.capital_costs['wind']['Initial capital cost'],
                          self.capital_costs['wind']['Yearly maintenance costs'],
                          self.session_time,
                          self.run_num,
                          self.user_id
                         )

        t_end = time.time()
        print(f'Done importing capital costs to server in {t_end-t_begin} seconds')
                                  
        #-----------------------------------------------------------------------------------------------------------
        #Calculate cumulative cost values for each generator for the next 10 years

        t_begin = time.time()
                
        self.years = [i for i in range(0,11)]
        # print(self.years)
        
        self.piston_cumulative_cost = [ self.capital_costs['piston']['Initial capital cost'] + i*(
                                  self.capital_costs['piston']['Yearly maintenance costs']  +
                                  self.capital_costs['piston']['Yearly fuel costs']) for i in self.years]
        # print(self.piston_cumulative_cost)
        
        self.mgt_cumulative_cost = [ self.capital_costs['MGT']['Initial capital cost'] + i * (
                                  self.capital_costs['MGT']['Yearly maintenance costs']  +
                                  self.capital_costs['MGT']['Yearly fuel costs']) for i in self.years]

        self.hmgt_cumulative_cost = [ self.capital_costs['HMGT']['Initial capital cost'] + i * (
                                  self.capital_costs['HMGT']['Yearly maintenance costs']  +
                                  self.capital_costs['HMGT']['Yearly fuel costs']) for i in self.years]

        self.solar_cumulative_cost = [ self.capital_costs['solar']['Initial capital cost'] + i * (
                                  self.capital_costs['solar']['Yearly maintenance costs'] ) for i in self.years]

        self.wind_cumulative_cost = [ self.capital_costs['wind']['Initial capital cost'] + i * (
                                  self.capital_costs['wind']['Yearly maintenance costs'] ) for i in self.years]

        self.grid_elect_cumulative_cost = [ (1 + year) * (self.total_power_comsumption * self.elect_grid_cost_selected *
                                      (1 + year * (self.energy_inflation_selected/100))) for year in self.years]
        # print(self.grid_elect_cumulative_cost)

        t_end = time.time()
        print(f'Calcaulated cumulative costs in {t_end-t_begin} seconds')

        #-----------------------------------------------------------------------------------------------------------
        #Upload cumulative costs to server

        t_begin = time.time()
        # created_time = datetime.now()

        for i in range(0,len(self.years)):
             anvil.server.call('add_cumulative_costs',
                               self.years[i],
                               self.piston_cumulative_cost[i],
                               self.mgt_cumulative_cost[i],
                               self.hmgt_cumulative_cost[i],
                               self.solar_cumulative_cost[i],
                               self.wind_cumulative_cost[i],
                               self.grid_elect_cumulative_cost[i],
                               self.session_time,
                               self.run_num
                              )

        t_end = time.time()
        print(f'Done importing cumulative costs to server in {t_end-t_begin} seconds')
        #-----------------------------------------------------------------------------------------------------------
        #Create data frame with uploaded cumulative costs
        # anvil.server.call('cumulative_cost_df')
        # print('df done')

        #Delete cumulative costs table from server
        # anvil.server.call('delete_cumulative_costs')
        # print('Cumulative costs table deleted from server')


        #-----------------------------------------------------------------------------------------------------------        
        # cumulative_costs = [ piston_cumulative_cost, mgt_cumulative_cost, hmgt_cumulative_cost, solar_cumulative_cost, wind_cumulative_cost, grid_elect_cumulative_cost]

        # scatter_1 = go.Scatter(x = years,
        #                   y = piston_cumulative_cost,
        #                   line=dict(color='#2196f3'))
        # scatter_2 = go.Scatter(x = years,
        #                   y = mgt_cumulative_cost,
        #                   line=dict(color='#2196f3'))
        # self.plot_1.data = scatter_1
        # app_tables.comulative_costs.add_row(piston=piston_cumulative_cost[0])

        t_end_total = time.time()

        print(f'Total run time {t_end_total-t_begin_total} seconds')
        # anvil.server.call('explore')
        anvil.server.call('reset_inputs')
        open_form('Form2')
        

        

        
       
                                  
                                 
        

