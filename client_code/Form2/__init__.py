from ._anvil_designer import Form2Template
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Form2(Form2Template):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Any code you write here will run before the form opens.
        anvil.server.call('explore')
        fig1 = anvil.server.call('create_plots')
        self.plot_1.figure = fig1

    
        
    def button_1_click(self, **event_args):
        """This method is called when the button is clicked"""
        # pass
        open_form('Form1')
        


        

