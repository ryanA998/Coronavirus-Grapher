
#Better version of the data handling file 
#Author: Ryan Arendt
#Last Edited: 10/18/2020

#Note: 
#   Need to change some of the documentation on the functions so that it 
#   sounds less awkward. I did it now because I want to get into the 
#   habit of documenting my code. (even if its awkward at first)

import csv 

def gen_graph_data(states_dict, state, data_catagory): 
    """ n order to graph the data: we need to lists. This function takes in the state abrivation
        and data catagory and returns a tuple contain the x and y values to graph. Where:
            x_data: (int) list of number of days since the begining of the pandemic 
            y_data: (int) list of number of people that fell under that catory for each day
    """
    #The above sounds a little awkward and can be changed. 


    x_data = [] 
    y_data = []

    #The problem is that some cells are empty in the CSV file. 
    #Espeically in the begining of the pandemic. IF the cell is empty: 
    #just add zero. 

    for i in range(0, len(states_dict[state][data_catagory])): 

        x_data.append(i)
        if states_dict[state][data_catagory][i] == "":
            y_data.append(0)
        else:

            y_data.append(int(states_dict[state][data_catagory][i]))
    
    #The data should be from earlist date -> current date vs. how it was originally, 
    #which was current date -> start date. 
    y_data = reverse_list(y_data)

    return (x_data, y_data) 


def reverse_list(lst):
    """ This is a helper function needed to graph the data since we usually want to 
        graph data from the start of the pandemic to the current date. However the data 
        from the csv file is "top-down" ie. from the current date to the start of the padnemic,
        we want to reverse that."""
    lst.reverse()
    return lst



def gen_covid_data(): 
    """ This function should read in the raw csv file that contains the covid data for each state
        during each day of the pandemic (so far) and should output a dictionary of dictionaries that
        catagories the data based on state, data-catagoy and list of values for the pandemic
    """
    #Again: Im a bit tired and this sounds awkard. CHANGE.

    file_name = 'all-states-history.csv'
    state_names = [ 'AK','AL','AR','AS','AZ','CA','CO','CT','DC','DE','FL','GA','GU','HI','IA','ID','IL','IN','KS','KY',	
                'LA','MA','MD','ME','MI','MN','MO','MP','MS','MT','NC','ND','NE','NH','NJ','NM','NV','NY','OH','OK',
                'OR','PA','PR',	'RI','SC','SD','TN','TX','UT','VA','VI','VT','WA','WI','WV','WY']
    
    dict_of_states = gen_dic_data_structure(state_names)

    #List of the index of each data catory in the csv file. It's important to speicify this because its
    #easy to forget. Also we may want to add catgories later.
    date_idx = 0
    death_idx = 3
    death_inc_idx = 5
    tot_hosp_idx = 7
    cur_hosp_idx = 9 
    hosp_inc_idx = 10 
    tot_icu_idx = 11
    cur_icu_idx = 12
    neg_idx = 13
    neg_inc_idx = 14
    tot_pos_idx = 21
    pos_inc_idx = 23

    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file)

        for row in csv_reader: 
            
            cur_state = row[1]
            #We want to skip the first row (contains headings) so we only look at state abrivations
            #that are length 2. All state abrivations [AL, IL, MN...etc] are of length two vs. the heading
            #"state" is length 4. There probably is a more elegant way to do this but it works.
            if len(cur_state) == 2:
                dict_of_states[cur_state]['date'].append(row[date_idx])
                dict_of_states[cur_state]['death'].append(row[death_idx])
                dict_of_states[cur_state]['death_increase'].append(row[death_inc_idx])
                dict_of_states[cur_state]['total_hospitalized'].append(row[tot_hosp_idx])
                dict_of_states[cur_state]['currently_hospitalized'].append(row[cur_hosp_idx])
                dict_of_states[cur_state]['hospitalized_increase'].append(row[hosp_inc_idx])
                dict_of_states[cur_state]['total_icu'].append(row[tot_icu_idx])
                dict_of_states[cur_state]['current_icu'].append(row[cur_icu_idx])
                dict_of_states[cur_state]['negative_test'].append(row[neg_idx])
                dict_of_states[cur_state]['negative_test_increase'].append(row[neg_inc_idx])
                dict_of_states[cur_state]['total_positive'].append(row[tot_pos_idx])
                dict_of_states[cur_state]['increase_positive_cases'].append(row[pos_inc_idx])
                
    return dict_of_states
            


def gen_dic_data_structure(state_name_abbrvs): 
    """ Generates the skeleton of the dictionary data structure needed for the program. We
        want a dictionary of dictionaries where:

        outer dictionary -> keys: abrivations for each state
                            values: dictionary of the catagories of data
        
        inner dictionary -> keys: catagories of data 
                            values: list of values since beginning of pandemic
    """

    states_data_structure = {}

    for name in state_name_abbrvs: 
        states_data_structure[name] = {'date': [],'death': [],'death_increase': [],'total_hospitalized': [], 'currently_hospitalized': [],
                 'hospitalized_increase': [],'total_icu': [], 'current_icu': [],'negative_test': [], 'negative_test_increase': [],
                 'total_positive': [],'increase_positive_cases': []}

    return states_data_structure