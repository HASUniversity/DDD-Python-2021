# import 
import raster_functions
import pandas as pd
import os
import csv

# Navigeer naar de "data" folder met de satellietbeelden
os.chdir(r'C:\git_repositories\DDD-Python-2021\data')

# Create empty lists waarin de locatie, datum en ndvi waarden worden bewaard.
datum_list = []
ndvi_list = []
locatie_list = []

# Iterate over locations 
# Zie: https://pythonprogramming.net/reading-csv-files-python-3/
i = 0
for inleeslocatie in open(r'inleeslocaties.csv') :
    
    # Skip first line
    if i > 0 :
        locatie_id = inleeslocatie.split(',')[0]
        x = float(inleeslocatie.split(',')[1])
        y = float(inleeslocatie.split(',')[2])

        # Itereer over de rasterbestanden van band 4 to calculate NDVI
        for file_name in os.listdir() :
            if 'NDVI' in file_name and os.path.splitext(file_name)[1] == '.tif' : 

                # Check coordinaatsysteem
                if raster_functions.get_coordinate_system(file_name) == '28992' :
                    print('Coordinate transformation')
                    raster_functions.transform_raster_image(file_name,32631)
                
                # Get NDVI value
                datum = file_name[15:23]
                NDVI_value = raster_functions.get_value_from_raster(file_name, x, y)
                print(str(locatie_id) + ': ' + str(datum) + ': ' + str(NDVI_value))
                datum_list.append(datum)
                ndvi_list.append(NDVI_value)
                locatie_list.append(locatie_id)

    i = i + 1
    
# Voeg lijsten samen tot dataframe
df = pd.DataFrame(list(zip(datum_list, ndvi_list, locatie_list)), columns =['datum', 'ndvi', 'loc']) 
print(df.head(5))

# Export to Excel and CSV
df.to_excel('NDVI_loc.xlsx', index = False)
df.to_csv('NDVI_loc.csv', index = False)