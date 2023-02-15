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

        #-----------------------------------------------------------------------------------------------------------
        #Variables drop down menus:
        avg_power = [20, 30, 40, 60, 75, 100, 125, 135, 150, 175, 200]
        avg_power_str = [str(item) for item in avg_power]
        self.dd_avg_power.items = avg_power_str
        self.dd_avg_power.selected_value = '30' #Default value
        # print(avg_power_str)
        # print(f'Average power\n{avg_power}\n')
        
        run_time = [ item for item in range(1, 24+1) ]
        run_time_str = [str(item) for item in run_time]
        self.dd_run_time.items = run_time_str
        self.dd_run_time.selected_value = '8' #Default value
        # print(f'Run time\n{run_time}\n')
        
        days_year = [ item for item in range(1, 365+1)]
        days_year_str = [str(item) for item in days_year]
        self.dd_days_year.items = days_year_str
        self.dd_days_year.selected_value = '250' #Default value
        # print(f'Days of the year operating\n{days_year}\n')
        
        
        solar_irrad = [1.5, 2.6, 3, 4, 5.45, 6]
        solar_irrad_str = [str(item) for item in solar_irrad]
        self.dd_solar_irrad.items = solar_irrad_str
        self.dd_solar_irrad.selected_value = '5.45' #Default value
        # Solar radiation can be categorized into four classes: levels less than 2.6 kWh/m2 
        # are classified as low solar radiation while solar irradiance between 2.6-3 kWh/m2 
        # is moderate solar radiation; irradiance of between 3-4 kWh/m2 is high solar radiation
        # and irradiance higher than 4 kWh/m2 is very high radiation.
        # print(f'Average solar irradiation\n{solar_irrad}\n')
        
        wind_speed = [item for item in range(2, 15+1)]
        wind_speed_str = [str(item) for item in wind_speed]
        self.dd_wind_speed.items = wind_speed_str
        self.dd_wind_speed.selected_value = '5' #Default value
        # print(f'Average wind speed\n{wind_speed}\n')
        
        fuel_cost = [1 + (item/10) for item in range(0, 11) ]
        fuel_cost_str = [str(item) for item in fuel_cost]
        self.dd_fuel_cost.items = fuel_cost_str
        self.dd_fuel_cost.selected_value = '1.0' #Default value
        # print(f'Average fuel cost\n{fuel_cost}\n')
        
        elect_grid_cost = [round((3 + (item/10))/10, 2) for item in range(4, 70)]
        elect_grid_cost_str = [str(item) for item in elect_grid_cost]
        self.dd_elect_grid_cost.items = elect_grid_cost_str
        self.dd_elect_grid_cost.selected_value = '0.34' #Default value
        # print(f'Electric grid cost\n{elect_grid_cost}\n')

        energy_inflation = [ item for item in range(10, 101, 10)]
        energy_inflation_str = [str(item) for item in energy_inflation]
        self.dd_energy_inflation.items = energy_inflation_str
        self.dd_energy_inflation.selected_value = '30' #Default value
        # print(f'Energy inflation\n{energy_inflation}\n')
        

    def run_button_click(self, **event_args):      
        
        """This method is called when the button is clicked"""
        #-----------------------------------------------------------------------------------------------------------
        #Selected values:
        
        avg_power_selected = anvil.server.call('str_to_num', self.dd_avg_power.selected_value)
        run_time_selected = anvil.server.call('str_to_num',self.dd_run_time.selected_value)
        days_year_selected = anvil.server.call('str_to_num',self.dd_days_year.selected_value)
        solar_irrad_selected = anvil.server.call('str_to_num',self.dd_solar_irrad.selected_value)
        wind_speed_selected = anvil.server.call('str_to_num',self.dd_wind_speed.selected_value)
        fuel_cost_selected = anvil.server.call('str_to_num',self.dd_fuel_cost.selected_value)
        elect_grid_cost_selected = anvil.server.call('str_to_num',self.dd_elect_grid_cost.selected_value)
        energy_inflation_selected = anvil.server.call('str_to_num',self.dd_energy_inflation.selected_value)
        
        #-----------------------------------------------------------------------------------------------------------
        #Outputs
        
        total_power_comsumption = avg_power_selected*run_time_selected*days_year_selected
        # print(f'Total power comsumption: {total_power_comsumption} kWh')

        #-----------------------------------------------------------------------------------------------------------
        #Generate capital costs dictionary for all power generators:
        capital_costs = {}
        generators = ['piston', 'MGT', 'HMGT', 'solar', 'wind']
        cost_factor = {'piston': 0.15, 'MGT': 0.0045, 'HMGT': 0.0045, 'solar':3000, 'wind': 0.0082}

        #Get column names from app tables
        column_generator_costs = app_tables.generator_cost.list_columns()[1]['name'] #column 'pounds_per_kwh' in table 3
        column_generator_efficiency = [app_tables.generator_efficiency.list_columns()[i]['name'] for i in range(1, 4)] #efficiency columns 45, 35 and 50 in table 2
        # print(column_generator_efficiency)

        generator_efficiency_obj = app_tables.generator_efficiency.get(generator_size=avg_power_selected)
        # print(f'gen eff{generator_efficiency_obj}')

        for item in generators:
            #Object for table row 
            generator_cost_obj = app_tables.generator_cost.get(generator=item)
            capital_costs[item] = {'Initial capital cost': generator_cost_obj[column_generator_costs]*avg_power_selected}
            if item == 'solar':
                capital_costs[item]['Yearly maintenance costs'] = cost_factor['solar']
            else:
                capital_costs[item]['Yearly maintenance costs'] = total_power_comsumption*cost_factor[item]
                
            if item not in ['solar', 'wind']: 
                if item == 'piston':
                    efficiency = '45'
                elif item == 'MGT':
                    efficiency = '35'
                elif item == 'HMGT':
                    efficiency = '50'      
                fuel_data = app_tables.generator_efficiency.get(generator_size=avg_power_selected)[efficiency]
                # print(f'fuel data: {fuel_data}')
                capital_costs[item]['Yearly fuel costs'] = fuel_data*run_time_selected*days_year_selected*fuel_cost_selected       
        print(capital_costs)
        #-----------------------------------------------------------------------------------------------------------
        #Calculate cumulative cost values for each generator for the next 20 years
                
        # years = [i for i in range(0,21)]
        # print(years)
        
        # piston_cumulative_cost = [ capital_costs['piston']['Initial capital cost'] + i*(
        #                           capital_costs['piston']['Yearly maintenance costs']  +
        #                           capital_costs['piston']['Yearly fuel costs']) for i in years]
        # print(piston_cumulative_cost)
        
        # mgt_cumulative_cost = [ capital_costs['MGT']['Initial capital cost'] + i * (
        #                           capital_costs['MGT']['Yearly maintenance costs']  +
        #                           capital_costs['MGT']['Yearly fuel costs']) for i in years]

        # hmgt_cumulative_cost = [ capital_costs['HMGT']['Initial capital cost'] + i * (
        #                           capital_costs['HMGT']['Yearly maintenance costs']  +
        #                           capital_costs['HMGT']['Yearly fuel costs']) for i in years]

        # solar_cumulative_cost = [ capital_costs['solar']['Initial capital cost'] + i * (
        #                           capital_costs['solar']['Yearly maintenance costs'] ) for i in years]

        # wind_cumulative_cost = [ capital_costs['wind']['Initial capital cost'] + i * (
        #                           capital_costs['wind']['Yearly maintenance costs'] ) for i in years]

        # grid_elect_cumulative_cost = [ (1 + year) * (total_power_comsumption * elect_grid_cost_selected *
        #                               (1 + year * (energy_inflation_selected/100))) for year in years]
        # print(grid_elect_cumulative_cost)

        # cumulative_costs = [ piston_cumulative_cost, mgt_cumulative_cost, hmgt_cumulative_cost, solar_cumulative_cost, wind_cumulative_cost, grid_elect_cumulative_cost]

        # scatter_1 = go.Scatter(x = years,
        #                   y = piston_cumulative_cost,
        #                   line=dict(color='#2196f3'))
        # scatter_2 = go.Scatter(x = years,
        #                   y = mgt_cumulative_cost,
        #                   line=dict(color='#2196f3'))
        # self.plot_1.data = scatter_1
        # app_tables.comulative_costs.add_row(piston=piston_cumulative_cost[0])
        

        

        
       
                                  
                                 
        

