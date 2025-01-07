# module reads in tornado data from a csv file on weather storms from government

import csv

class TornadoStats():
    """
    class uses 2024 tornado data to predict the 
    2025 tornado data using math and stats calculations
    """

    def __init__(self, data):
        self.data = data
    
    def file_read(self):
        """
        reads in the csv file of tornado data
        """
        try:
            with open(self.data) as file:
                contents = csv.reader(file)
                content = [i for i in contents]
            return content
        except FileNotFoundError:
            return 'File cannot be found'
        
    def tornado_total(self):
        """
        reads the data from row 13 of the weather data csv file. 
        this data is the weather event (hurricane, heavy snow, tornado, etc.). 
        num_tornado is the total number of tornado for that year.
        """
        num_tornado = 0
        for i in self.file_read():
            if (len(i) >= 32) and (i[12] == 'Tornado'):
                num_tornado += 1
        return num_tornado
    
    def strength(self):
        """
        returns list of data from row 32 of weather data csv file
        containing the strength of each individual tornado.
        """
        ef = []
        for i in self.file_read():
            if (len(i) >= 32) and (i[12] == 'Tornado'):
                ef.append(i[31])
        return ef

    def strength_ratio(self):
        """
        reads data from row 32 of the weather data csv file.
        this data gives the strength of the storm. 
        tornado strength ranges from EFU -> EF5. 
        function returns ratio of each type of strenght in tuple 
        going in order from EFU -> EF5. 
        """
        efu = 0
        ef0 = 0
        ef1 = 0
        ef2 = 0
        ef3 = 0
        ef4 = 0
        ef5 = 0
        
        for i in self.strength():
            if (i == 'EFU') or (i == ''):
                efu += 1
            elif (i == 'EF0') or (i == 'F0'):
                ef0 += 1
            elif (i == 'EF1') or (i == 'F1'):
                ef1 += 1
            elif (i == 'EF2') or (i == 'F2'):
                ef2 += 1
            elif (i == 'EF3') or (i == 'F3'):
                ef3 += 1
            elif (i == 'EF4') or (i == 'F4'):
                ef4 += 1
            elif (i == 'EF5') or (i == 'F5'):
                ef5 += 1
        
        ratio_efu = efu / self.tornado_total()
        ratio_ef0 = ef0 / self.tornado_total()
        ratio_ef1 = ef1 / self.tornado_total()
        ratio_ef2 = ef2 / self.tornado_total()
        ratio_ef3 = ef3 / self.tornado_total()
        ratio_ef4 = ef4 / self.tornado_total()
        ratio_ef5 = ef5 / self.tornado_total()
        try:
            if round(ratio_efu + ratio_ef0 + ratio_ef1 + ratio_ef2 + ratio_ef3 + ratio_ef4 + ratio_ef5) != 1.0:
                raise ValueError
            else:
                return (ratio_efu, ratio_ef0, ratio_ef1, ratio_ef2, ratio_ef3, ratio_ef4, ratio_ef5)
        except ValueError:
            return 'Something is not correct...the ratios do not appear to add up to 1.0'
        

    def casualty_lists(self):
        """
        reads in data from rows 21 -> 24 in weather data csv file.
        these rows contain data on injuries and deaths (direct and indirect).
        returns a tuple of the lists of injures per tornado and list of deaths
        per tornado and list of casualties per tornado. 
        """
        injuries_list = []
        deaths_list = []
        casualties_list = []
        for i in self.file_read():
            if (len(i) >= 32) and (i[12] == 'Tornado'):
                injuries_list.append(float(i[20]))
                injuries_list.append(float(i[21]))
                deaths_list.append(float(i[22]))
                deaths_list.append(float(i[23]))
                casualties_list.append((float(i[20]) + float(i[21]) + float(i[22]) + float(i[23])))
        return (injuries_list, deaths_list, casualties_list)
    
    def cas_only_tor(self):
        """
        gives a tuple of a list of the tornadoes with casualties,
        the ratio of tornadoes with casualties,
        and the mean number of casualties for only tornadoes with 
        casualties. 
        """
        cas_only = []
        for i in self.casualty_lists()[2]:
            if i > 0.0:
                cas_only.append(i)
        
        ratio = len(cas_only) / self.tornado_total()

        mean_cas_only = sum(cas_only) / len(cas_only)

        string = f"{len(cas_only)}/{self.tornado_total()}"

        return(cas_only, ratio, mean_cas_only, string)

    def casualties(self):
        """
        uses the lists of injuries and deaths created and returned in 
        casualty_lists function to return a tuple of total
        (injures, deaths, casualties). 
        """
        injuries = sum(self.casualty_lists()[0])
        deaths = sum(self.casualty_lists()[1])
        casualties = injuries + deaths
        return (injuries, deaths, casualties)
    
    def damage_lists(self):
        """
        reads in data from row 25 from weather data csv file.
        gives list of property damage costs from each individual tornado.
        """
        damage_list = []
        convert_1 = []
        for i in self.file_read():
            if (len(i) >= 32) and (i[12] == 'Tornado'):
                convert_1.append(i[24])
        for i in convert_1:
            convert_3 = []
            for x in i:
                convert_3.append(x)
            if 'K' in i:
                convert_3.remove('K')
                convert_string = ""
                for i in convert_3:
                    convert_string += i
                convert_string_2 = float(convert_string) * 1000
            elif 'M' in i:
                convert_3.remove('M')
                convert_string = ""
                for i in convert_3:
                    convert_string += i
                convert_string_2 = float(convert_string) * 1000000
            damage_list.append(convert_string_2)
        return damage_list
    
    def total_damage(self):
        """
        returns total property damage costs using the list in 
        damage_lists function. 
        """
        total_costs = sum(self.damage_lists())
        return total_costs
        
    def lat_lon(self):
        """
        reads in data from rows 45 -> 46 from weather data csv file.
        data in row 45 is tornado beginning latitude and 46 is longitude. 
        function will return tuple of (x,y) coordinates.
        """
        latitude_list = []
        longitude_list = []
        latitude = []
        longitude = []
        coordinates =  []
        n = 0
        for i in self.file_read():
            if (len(i) >= 46) and (i[12] == 'Tornado'):
                latitude_list.append(i[44])
                longitude_list.append(i[45])
                for i in latitude_list:
                    latitude.append(float(i))
                for i in longitude_list:
                    longitude.append(float(i))
                coordinates_xy = (longitude[n], latitude[n])
                n += 1
                coordinates.append(coordinates_xy)
        return coordinates
    
    def state(self):
        """
        Tornado count per state
        """
        state = []
        for row in self.file_read():
            if len(row) > 31:
                if row[12] == 'Tornado':
                    state.append(row[8])

        break_list = []
        num_s_list = []
        state_num = {}

        for i in state:
            if i not in break_list:
                num_s_list.append(i)
                break_list.append(i)

        for i in num_s_list:
            g = 0
            n = 0
            while n < len(state):
                if i == state[n]:
                    g+=1
                n+=1

            state_num[i] = g
        
        sorted_states = dict(sorted(state_num.items()))

        return(sorted_states)

    def data_specific(self, n):
        """
        gives data for a specific tornado (n).
        plug in (n) into the function --> returns
        data for the nth tornado of the year
        """
        self.n = n
        try:
            if (self.n <= self.tornado_total()) and (self.n > 0):
                string = f"Tornado Number: {self.n} / {self.tornado_total()}\n\
Strength: {self.strength()[(self.n) - 1]}\n\
Injuries: {(self.casualty_lists()[0])[(self.n) - 1]}\n\
Deaths: {(self.casualty_lists()[1])[(self.n) - 1]}\n\
Total Casualties: {(self.casualty_lists()[0][(self.n) - 1]) + ((self.casualty_lists()[1])[(self.n) - 1])}\n\
Property Damage Costs: ${self.damage_lists()[(self.n) - 1]}\n\
Coordinates of Start (longitude, latitude): {self.lat_lon()[(self.n) - 1]}"
            else:
                raise ValueError
        except ValueError:
            string = "n must be in the range of the total tornadoes for selected year"
        finally:
            return string
        
    def summary_stats(self):
        """
        summary of the tornado stats for selected year.
        """
        string = f"Total Tornadoes: {self.tornado_total()}\n\
Total Injuries: {self.casualties()[0]}\n\
Total Deaths: {self.casualties()[1]}\n\
Total Casualties: {self.casualties()[2]}\n\
Tornadoes With Casualties: {self.cas_only_tor()[-1]}\n\
Mean Casualties Per Tornado With Casualties: {self.cas_only_tor()[2]}\n\
Total Property Damage Costs: ${self.total_damage()}"
        return string


# Example code using a file in the folder to call the class funcitons
tor_dat = 'storm_events_2010.csv'
work = TornadoStats(tor_dat)



