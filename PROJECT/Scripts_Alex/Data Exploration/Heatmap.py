import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gp


H5_INFILE = "S:/1-TNCs and Transit Ridership/Ridership Model Results/TOD Models/Bus Model/sfmuni_monthly_ts.h5"
BASE_START_DATE = '2009-09-01'
BASE_END_DATE = '2009-12-01'
FUTURE_START_DATE = '2016-09-01'
FUTURE_END_DATE = '2016-12-01'
DIRECTIONS = [1,0]


OUTFILE_START = 'S:/1-TNCs and Transit Ridership/DataExploration/HeatMaps/2009 and 2016/Stop Heatmaps/'

def create_heatmap(df,direction):
    """
    function to create a heatmap of a route given a pivot table with time (TOD) as the columns and 
    stopnames as the row index
    
    df = dataframe of route 
    direction = direction of the route (1 or 0 for inbound and outbound)
    """
    
    plt.figure(figsize =(10, 10))
    if direction == 1:
        plt.title('ROUTE ' + str(route) + ' (Inbound)')
        plt.tight_layout()
        Heatmap = sns.heatmap(df, robust = True, cmap = 'RdYlGn',fmt = '.1f',annot = False,
                              linecolor = 'black',linewidth = 0.1,cbar = True,square = False, 
                              xticklabels = True, yticklabels = True)
        Heatmap.set_yticklabels(Heatmap.get_yticklabels(), rotation = 0, fontsize = 8)
        
    elif direction == 0:
        plt.title('ROUTE ' + str(route) + ' (Outbound)')
        plt.tight_layout()
        Heatmap = sns.heatmap(df, robust = True, cmap = 'RdYlGn',fmt = '.1f',annot = False,
                              linecolor = 'black',linewidth = 0.1,cbar = True,square = False, 
                              xticklabels = True, yticklabels = True)
        Heatmap.set_yticklabels(Heatmap.get_yticklabels(), rotation = 0, fontsize = 8)
        
    else:
        print('Bad Direction!')

    return Heatmap
 
 
    
if __name__ == "__main__":
    # read in the monthly route stops table
    store = pd.HDFStore(H5_INFILE)
    bus = store.get('rs_tod')
    
    #select out the months that are of interest
    bus09 = bus[bus["MONTH"].isin(pd.date_range(BASE_START_DATE,BASE_END_DATE))]
    bus09['ROUTE_SHORT_NAME2'] = bus09.ROUTE_SHORT_NAME
    
    bus13 = bus[bus['MONTH'].isin(pd.date_range(FUTURE_START_DATE,FUTURE_END_DATE))]
    bus13['ROUTE_SHORT_NAME2'] = bus13.ROUTE_SHORT_NAME
    bus13.ROUTE_SHORT_NAME2[bus13.ROUTE_SHORT_NAME2 == '5R'] = '5L'
    bus13.ROUTE_SHORT_NAME2[bus13.ROUTE_SHORT_NAME2 == '7R'] = '7L'
    bus13.ROUTE_SHORT_NAME2[bus13.ROUTE_SHORT_NAME2 == '9R'] = '9L'
    bus13.ROUTE_SHORT_NAME2[bus13.ROUTE_SHORT_NAME2 == '14R'] = '14L'
    bus13.ROUTE_SHORT_NAME2[bus13.ROUTE_SHORT_NAME2 == '28R'] = '28L'
    bus13.ROUTE_SHORT_NAME2[bus13.ROUTE_SHORT_NAME2 == '38R'] = '38L'
    bus13.ROUTE_SHORT_NAME2[bus13.ROUTE_SHORT_NAME2 == '43R'] = '43L'


    
    
    #merge the two dataframes to calculate a difference between the two date ranges (years)
    bus_diff = pd.merge(bus09,bus13,how = 'inner',
                        on =['DOW','TOD','AGENCY_ID','ROUTE_SHORT_NAME2','DIR','SEQ'],suffixes = ('_09','_13'))
                        
    bus_diff['DIFF'] = (bus_diff['ON_13'] + bus_diff['OFF_13'])/2 - (bus_diff['ON_09'] + bus_diff['OFF_09'])/2
    
    #set count to keep track of what dataframe is being processed
    bus_dfs = [bus09,bus13,bus_diff]
    count = 0
    
    #run through all of the dataframes
    for bus_df in bus_dfs:
        print('Started new heatmaps dataframe')
        
        #run through all of the routes
        for route in bus_df['ROUTE_SHORT_NAME2'].unique():
            print('Started route ' + route)
            
            #run through all of the directions (inbound and outbound)
            for direction in DIRECTIONS:
                
                #select out the rows of interest
                route_df = bus_df[(bus_df['ROUTE_SHORT_NAME2'] == route) & (bus_df['DIR'] == direction)]
                
                #if there are no rows in the dataset for a particular route in a particular direction then 
                #the route is assumed to not run in that direction
                
                if len(route_df) == 0:
                    print('Route ' + route + ' in ' + str(direction) + ' direction does not run')
                else:
                
                    #create a pivot table in the form required for the heatmap, use stopname as the index 
                    #because it is easier to recognize
                    if count != 2: 
                        pivot = route_df.pivot_table(values = 'LOAD_DEP',index = 'STOPNAME',
                                              columns = 'TOD',aggfunc = 'sum',margins = False, fill_value = 0)
                    #create the heatmap  
                        heatmap = create_heatmap(pivot,direction)
                        figure = heatmap.get_figure()
                        
                        #save the heatmap
                        if count == 0:
                            figure.savefig(OUTFILE_START  + '2009 ' + str(route) + '_' + 'Route ' +
                            str(direction) + '.jpg',bbox_inches='tight',pad_inches = 6)
                        elif count == 1:
                            figure.savefig( OUTFILE_START + ' 2016 ' + str(route) + '_' + 'Route ' +
                            str(direction) + '.jpg',bbox_inches='tight',pad_inches = 6)
                        else:
                            print('Something is wrong')
                    else:
                        
                        #create a similar pivot table as before, but instead use sequence because stop names may 
                        #change between years
                        pivot = route_df.pivot_table(values = 'DIFF',index = 'SEQ',
                                              columns = 'TOD',aggfunc = 'sum',margins = False, fill_value = 0)
                                              
                        heatmap = create_heatmap(pivot,direction)
                        figure = heatmap.get_figure()
                        figure.savefig(  OUTFILE_START + 'Diff ' + str(route) + '_' + 'Route ' +
                        str(direction) + '.jpg',bbox_inches='tight')
                     
                   
                plt.close('all')
        count = count + 1        
            
                
    print('ALL DONE TIME FOR HALO!')
