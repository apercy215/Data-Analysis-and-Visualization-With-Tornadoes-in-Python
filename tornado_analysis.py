# module analyzes tornado data using the tornado.py file that read in tornado data

# correlation main look: between location vs casualties/damage and strength vs casualties/damage
# as well as location vs strength

import numpy as np
import scipy.stats as sp
import matplotlib.pyplot as plt
from tornado import TornadoStats as ts

class R_analysis():
    """
    Class uses tornado.py module to analyze tornado data
    and create visual representations. 
    """

    def __init__(self, data):
        """
        Initialize data from tornado.py module. 
        """
        self.data = data
    
    def damage_vs_casualties(self):
        """
        Damage costs for a tornado vs casualties for that tornado. 
        Creates a scatterplot representing property damage on the 
        x-axis and casulaties on the y-axis with a trendline to 
        show correlation. 
        """

        cas = sorted(self.data.casualty_lists()[2])
        dam = sorted(self.data.damage_lists())
        max_cas = cas[-1]
        max_dam = dam[-1]

        y = self.data.casualty_lists()[2]
        x = self.data.damage_lists()

        q1x = np.percentile(x, 25)
        q3x = np.percentile(x, 75)
        iqrx = q3x - q1x

        q1y = np.percentile(y, 25)
        q3y = np.percentile(y, 75)
        iqry = q3y - q1y

        outx = q1x - (1.5*iqrx)
        outy = q1y - (1.5*iqry)
        out2x = q3x + (1.5*iqrx)
        out2y = q3y + (1.5*iqry)

        new_x = []
        new_y = []
        p = 0
        while p < len(x):
            if ((x[p] > outx) or (x[p] < out2x)) or ((y[p] > outy) or (y[p] < out2y)):
                new_x.append(x[p])
                new_y.append(y[p])
            p+=1
        
        
        slope, intercept, r_value, p_value, std_err = sp.linregress(new_x, new_y)

        line = [slope * i + intercept for i in new_x]
        
        plt.scatter(new_x, new_y)
        plt.plot(new_x, line, color ="red", label = f"trendline r = {r_value}")
        plt.legend()
        plt.title('Damage Costs vs. Casualties from US Tornado Anaual Data')
        plt.xlabel('Damage in $Millions')
        plt.ylabel('Casualties')
        plt.show()
            
    def strength_vs_mean_casualties(self):
        """
        Casualties vs Strength of tornado. 
        Creates a bar graph showing the mean casualties per
        tornado of a specific strength (EFU --> EF5). 
        only for tonradoes with casulaties. 
        """
        new_strength = ts.strength(self.data)
        strength1 = []
        for i in new_strength:
            if i not in strength1:
                strength1.append(i)

        strength = ['EFU', 'EF0', 'EF1', 'EF2', 'EF3', 'EF4', 'EF5']

        eU = []
        e0 = []
        e1 = []
        e2 = []
        e3 = []
        e4 = []
        e5 = []
        h = 0
        m = 0
        while h < len(ts.casualty_lists(self.data)[2]):
            if (ts.strength(self.data)[h] == 'EFU') or (ts.strength(self.data)[h] == ''):
                if ts.casualty_lists(self.data)[2][h] > 0.0:
                    eU.append((ts.casualty_lists(self.data)[2])[h])

            elif (ts.strength(self.data)[h] == 'EF0') or (ts.strength(self.data)[h] == 'F0'):
                if ts.casualty_lists(self.data)[2][h] > 0.0:
                    e0.append((ts.casualty_lists(self.data)[2])[h])

            elif (ts.strength(self.data)[h] == 'EF1') or (ts.strength(self.data)[h] == 'F1'):
                if ts.casualty_lists(self.data)[2][h] > 0.0:
                    e1.append((ts.casualty_lists(self.data)[2])[h])

            elif (ts.strength(self.data)[h] == 'EF2') or (ts.strength(self.data)[h] == 'F2'):
                if ts.casualty_lists(self.data)[2][h] > 0.0:
                    e2.append((ts.casualty_lists(self.data)[2])[h])

            elif (ts.strength(self.data)[h] == 'EF3') or (ts.strength(self.data)[h] == 'F3'):
                if ts.casualty_lists(self.data)[2][h] > 0.0:
                    e3.append((ts.casualty_lists(self.data)[2])[h])

            elif (ts.strength(self.data)[h] == 'EF4') or (ts.strength(self.data)[h] == 'F4'):
                if ts.casualty_lists(self.data)[2][h] > 0.0:
                    e4.append((ts.casualty_lists(self.data)[2])[h])

            elif (ts.strength(self.data)[h] == 'EF5') or (ts.strength(self.data)[h] == 'F5'):
                if ts.casualty_lists(self.data)[2][h] > 0.0:
                    e5.append((ts.casualty_lists(self.data)[2])[h])

            h+=1

        if len(eU) != 0:
            meanU = sum(eU) / len(eU)
        else:
            meanU = 0
        if len(e0) != 0:
            mean0 = sum(e0) / len(e0)
        else:
            mean0 = 0
        if len(e1) != 0:
            mean1 = sum(e1) / len(e1)
        else:
            mean1 = 0
        if len(e2) != 0:
            mean2 = sum(e2) / len(e2)
        else:
            mean2 = 0
        if len(e3) != 0:
            mean3 = sum(e3) / len(e3)
        else:
            mean3 = 0
        if len(e4) != 0:
            mean4 = sum(e4) / len(e4)
        else:
            mean4 = 0
        if len(e5) != 0:
            mean5 = sum(e5) / len(e5)
        else:
            mean5 = 0

        mean_list = [meanU, mean0, mean1, mean2, mean3, mean4, mean5]

        for i, mean in enumerate(mean_list):
            plt.text(i, mean + 0.15, str(round(mean,2)), ha='center', va='bottom', fontsize=10)

        plt.bar(strength, mean_list, color='blue', alpha=0.7)
        plt.title('Casualties vs. Strength from US Tornado Anaual Data')
        plt.xlabel('Tornado Strength (EFU --> EF5)')
        plt.ylabel('Mean Casualties Per Tornado')
        plt.show()
            
    def location_analysis(self):
        """
        Heatmap of tornado location based on lat/lon coordinates in US. 
        Graphical representation also plots the US border for unique 
        visual reference. 
        """
        
        lat_list = [i[1] for i in ts.lat_lon(self.data)]
        lon_list = [i[0] for i in ts.lat_lon(self.data)]
        
        import geopandas as gpd

        shapefile_path = "/Users/alexpercy/Downloads/ne_110m_admin_0_countries-2/ne_110m_admin_0_countries.shp"
        world = gpd.read_file(shapefile_path)

        
        usa = world[world['NAME'] == 'United States of America']
        continential_usa = usa.cx[-125.0:-66.93457, 24.396308:49.384358]

        fig, ax = plt.subplots(figsize=(12, 8))

        continential_usa.boundary.plot(ax=ax, color="blue", linewidth=1)
       
        x = lon_list
        y = lat_list

        ax.scatter(x, y, color="red", marker="o", alpha=0.5, label="Tornado Hot Spots", s=30)
        ax.set(xlim = (-130, -60), ylim = (20, 55))
        ax.set_title("Continential United States with Overlayed Tornado Coordinates")
        ax.set_xlabel("Longitude")
        ax.set_ylabel("Latitude")
        ax.grid(True)
        ax.legend()

        plt.show()

    def state_analysis(self):
        """
        Bar graph of the number of tornado spawns in each 
        US state over the year. 
        """

        x = []
        y = []
   

        for i in ts.state(self.data).keys():
            x.append(i)
        for i in ts.state(self.data).values():
            y.append(i) 

        plt.figure(figsize=(10,8))
        plt.bar(x, y, color='blue', alpha=0.7)
        plt.title('Tornadoes per State from US Tornado Data')
        plt.xlabel('State')
        plt.ylabel('Tornadoes Per State')
        plt.xticks(rotation=90, fontsize=7) 
        plt.tight_layout()
        plt.show()

# Example code using a file in the folder to call the class funcitons
tor_dat = 'storm_events_2010.csv'
work = ts(tor_dat)

cor = R_analysis(work)


