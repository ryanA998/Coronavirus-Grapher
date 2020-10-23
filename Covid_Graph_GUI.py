#First Version of the Coronavirus Graphing Program
#Author: Ryan Arendt
#Last Edited: 10/18/2020 

import sys 

from PyQt5 import QtWidgets 
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QComboBox, QPushButton, QWidget, QVBoxLayout, QGridLayout
import pyqtgraph as pg 

from Covid_Data import gen_covid_data, gen_graph_data
from functools import partial

class Main_Window(QMainWindow):

    def  __init__(self, graph_data):
        super().__init__()

        #Initalizes ALL of the historical data for the states. 
        self.graph_data = graph_data

        #Window Settings
        self.setWindowTitle("Graph of Coronavirus Data: States vs. Days Since Beginning of Pandemic")
        self.window_x_pos = 100
        self.window_y_pos = 100
        self.window_width = 800
        self.window_height = 500
        self.setGeometry(self.window_x_pos, self.window_y_pos, self.window_width, self.window_height)

        #Note: not 100% sure if I want to use a grid layout. Also not 100 sure
        #how the parameters work. Going to keep it for now. 
        self.graph_widget = QtWidgets.QWidget() 
        self.layout = QGridLayout()
        self.graph_widget.setStyleSheet(""" 
            QPushButton{
                border: 1px solid black;
                border-radius: 2px;
            }
            QComboBox{
                border: 1px solid gray;
                width: 140px;
                border-radius: 2px;
            }
            
        """)

        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

      

        self.graph_widget.setLayout(self.layout)

        self.setCentralWidget(self.graph_widget)

        #x and y values for the graph: initalized to be empty we change these later
        #Initailly want an empty graph until the users decides 
        self.x_values = [] 
        self.y_values = [] 

        #Calls each function to build the GUI interface 
        #self.add_graph() 
        self.add_state_dropdown()
        self.add_catagory_dropdown()
        self.add_button()
        self.add_graph() 
        

    def add_graph(self):
        """Should display Pandemic numbers vs. days since beginning of pandemic
        """
        graph_row = 0
        graph_row_span = 3
        graph_column = 2
        graph_column_span = 1

        #The region that the graph is plotten on. Review this to make sure
        graph_window = pg.plot()

        graph_window.showGrid(x=True, y=True)
        graph_window.setLabel('bottom', 'Days Since Begining of Pandemic')
    
        covid_graph = pg.BarGraphItem(x=self.x_values, height=self.y_values, width=0.90)

        graph_window.addItem(covid_graph)

        #row, column, rowspan, columnspan
        self.layout.addWidget(graph_window, graph_row, graph_column, graph_row_span, graph_column_span)


    #Note: should each widget component have self? Attached to it?
    def add_state_dropdown(self):
        state_names = [ 'AK','AL','AR','AS','AZ','CA','CO','CT','DC','DE','FL','GA','GU','HI','IA','ID','IL','IN','KS','KY',	
                'LA','MA','MD','ME','MI','MN','MO','MP','MS','MT','NC','ND','NE','NH','NJ','NM','NV','NY','OH','OK',
                'OR','PA','PR',	'RI','SC','SD','TN','TX','UT','VA','VI','VT','WA','WI','WV','WY']

        dropdown_box_row = 0
        dropdown_box_column = 0
        dropdown_box_row_span = 1
        dropdown_box_column_span = 1

        self.state_dropdown = QComboBox(self)
        self.state_dropdown.addItems(state_names)

        #This references the layout in the init function. So we probably need to keep that
        self.layout.addWidget(self.state_dropdown, dropdown_box_row, dropdown_box_column, dropdown_box_row_span, dropdown_box_column_span)


    def add_catagory_dropdown(self):

        data_catagories = ['Deaths','Increase in Deaths','Total Hospitalizations','Currently Hospitalized', 'Increase in Hospitalizations',
                'Total in ICU', 'Currently in ICU','Total Negative Tests','Negative Test Increase','Total Positive Tests','Positive Test Increase']
    
        dropdown_box_row = 1
        dropdown_box_column = 0
        dropdown_box_row_span = 1
        dropdown_box_column_span = 1

        self.catagory_dropdown = QComboBox(self)
        self.catagory_dropdown.addItems(data_catagories)

        self.layout.addWidget(self.catagory_dropdown, dropdown_box_row, dropdown_box_column, dropdown_box_row_span, dropdown_box_row_span)

    def add_button(self):
        
        button_row = 3
        button_column = 0
        button_row_span = 1 
        button_column_span = 1

        update_button = QPushButton("Update")
        update_button.pressed.connect(self.button_function)

        self.layout.addWidget(update_button, button_row, button_column, button_row_span, button_column_span)


    def button_function(self):
        
        #Note:  this map may be redundant. I could maybe change the names of the original data but doing so this
        #       way can allow us to have longer more descriptive names for the data

        #We need a map between the dropdown catagories and the dictionary catagory
        drop_down_map = {'Deaths':'death', 'Increase in Deaths':'death_increase', 'Total Hospitalizations':'total_hospitalized',
        'Currently Hospitalized': 'currently_hospitalized','Increase in Hospitalizations':'hospitalized_increase',
        'Total in ICU':'total_icu','Currently in ICU':'current_icu', 'Total Negative Tests':'negative_test',
        'Negative Test Increase':'negative_test_increase','Total Positive Tests':'total_positive','Positive Test Increase':'increase_positive_cases'

        }

        state_name = self.state_dropdown.currentText()

        dropdown_value = self.catagory_dropdown.currentText()

        data_catagory = drop_down_map[dropdown_value]

        graph_values = gen_graph_data(self.graph_data, state_name, data_catagory)

        self.x_values = graph_values[0]
        self.y_values = graph_values[1]
        self.add_graph()

def main():
    
    states_data = gen_covid_data()

    covid_application = QApplication(sys.argv)

    main_gui = Main_Window(states_data)

    main_gui.show()

    sys.exit(covid_application.exec())




if __name__ == "__main__":
    main()