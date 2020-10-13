# TO DO: Improve function coordinate transformation and keep the same name

# Importeren van module voor toegang tot systeem variabelen en functies
import sys

# Importeren van module voor interactie met file system
import os 

# Importeren van module met mathematische functies
import math

# Importeren van module voor plotten van rasterbestanden
from matplotlib import pyplot

# Importeren van module om te werken met arrays
import numpy

# Test of GDAL/OGR geïnstalleerd is en toon versie
try:
    import gdal
    import gdalnumeric
    import gdalconst
    import ogr
    import osr
    print('GDAL/OGR installed')
    print('Versie is ' + str(gdal.VersionInfo('VERSION_NUM')))
except:
    sys.exit('ERROR: cannot find GDAL/OGR modules')


# Function to get number of rows of satellite image
def get_nr_of_rows( raster_bestand_naam ) :
    try:
        raster_bestand = gdal.Open(raster_bestand_naam)
        nr_rows = raster_bestand.RasterYSize
        raster_bestand = None
        return nr_rows
    except Exception as e: 
        raster_bestand = None
        print('Error function get_nr_of_rows')
        print(e)


# Function to get number of columns of satellite image
def get_nr_of_cols( raster_bestand_naam ) :
    try:
        raster_bestand = gdal.Open(raster_bestand_naam)
        nr_cols = raster_bestand.RasterXSize
        raster_bestand = None
        return nr_cols
    except Exception as e: 
        raster_bestand = None
        print('Error function get_nr_of_cols')
        print(e)

# Function to get EPSG code from satellite image
def get_coordinate_system( raster_bestand_naam ) :
    try:
        raster_bestand = gdal.Open(raster_bestand_naam)
        proj = osr.SpatialReference(wkt=raster_bestand.GetProjection())
        coordinate_system = proj.GetAttrValue('AUTHORITY',1)
        raster_bestand = None
        return coordinate_system
    except Exception as e: 
        raster_bestand = None
        print('Error function get_coordinate_system')
        print(e)


# Function to get cell dimensions of satellite image
def get_cell_dimensions( raster_bestand_naam ) :
    try:
        raster_bestand = gdal.Open(raster_bestand_naam)
        geotransform = raster_bestand.GetGeoTransform()
        cell_width = geotransform[1]
        cell_height = geotransform[5]
        raster_bestand = None
        return cell_width, cell_height
    except Exception as e: 
        raster_bestand = None
        print('Error function get_cell_dimensions')
        print(e)


# Function to get upper left coordinate of satellite image
def get_ul_coordinate( raster_bestand_naam ) :
    try:
        raster_bestand = gdal.Open(raster_bestand_naam)
        geotransform = raster_bestand.GetGeoTransform()
        x_ul = geotransform[0]
        y_ul = geotransform[3]
        raster_bestand = None
        return x_ul, y_ul  
    except Exception as e: 
        raster_bestand = None
        print('Error function get_ul_coordinate')
        print(e)


# Function to plot raster file
def plot_raster( raster_bestand_naam ) :
    
    try: 

        # Load values from raster into array
        raster_bestand = gdal.Open(raster_bestand_naam, gdalconst.GA_ReadOnly)
        rasterband     = raster_bestand.GetRasterBand(1)
        array_band     = gdalnumeric.BandReadAsArray(rasterband)

        # Load array into pyplot and show plot with met colormap red
        pyplot.figure(figsize=(20,10))
        pyplot.imshow(array_band, cmap='Reds')
        pyplot.show()

    except Exception as e: 
        raster_bestand = None
        print('Error function plot_raster')
        print(e)

# Function to get value from raster on x,y location
def get_value_from_raster (raster_bestand_naam, x_in, y_in):

    try:
    
        # Open rasterbestand
        raster_bestand_in = gdal.Open(raster_bestand_naam)
        
        # Haal geotransform array op om geometrische eigenschappen rasterbestand op te halen
        nr_kolommen = int(raster_bestand_in.RasterXSize)
        nr_rijen = int(raster_bestand_in.RasterYSize)
        geotransform = raster_bestand_in.GetGeoTransform()
        x_links_boven = float(geotransform[0])
        y_links_boven = float(geotransform[3])
        cel_breedte = float(geotransform[1])
        cel_hoogte = float(geotransform[5])
        
        # Haal de eerste band op uit raster bestand
        rasterband = raster_bestand_in.GetRasterBand(1)

        # Laad het grid vanuit de rasterband in het array
        array = gdalnumeric.BandReadAsArray(rasterband)
        
        # Haal rij en kolom op
        kolom = int(math.ceil((x_in - x_links_boven)/cel_breedte))
        rij = int(math.ceil((y_in - y_links_boven)/cel_hoogte))
            
        # Check of waarde binnen raster valt
        if kolom > 0 and kolom <= nr_kolommen and rij > 0 and rij <= nr_rijen :
            waarde_uit = array[(rij-1),(kolom-1)]
        else :
            print('Opgegeven coördinaat ligt buiten raster')
            waarde_uit = None
        
        # Sluit raster bestand
        array = None
        raster_bestand_in = None
        
        # Geef waarde terug    
        return waarde_uit 

    except Exception as e: 
        raster_bestand_in = None
        print('Error function get_value_from_raster')
        print(e)

# Uitvoeren van coördinaattransformatie
def transform_raster_image (rasterfile_name_in, coordinate_system_to) :
    
    try:
    
        # Prepare transformation
        input_raster = gdal.Open(rasterfile_name_in)
        epsg_code = 'EPSG:' + str(coordinate_system_to)
        rasterfile_name_out = rasterfile_name_in[:-4] + '_' + str(coordinate_system_to) + '.tif'

        # Execute transformation
        out = gdal.Warp(rasterfile_name_out,input_raster,dstSRS=epsg_code)   
        input_raster = None
        out = None
        
        # Rename output file to input filename
        os.rename(rasterfile_name_in, rasterfile_name_in + '.old')
        os.rename(rasterfile_name_out, rasterfile_name_in)

    except Exception as e: 
        input_raster = None
        print('Error function transform_raster_image')
        print(e)


# Function to calculate NDVI rasterimage
def calculate_ndvi (rasterfile_red_name, rasterfile_nir_name) :
    
    try:
    
        # Construct name of NDVI rasterfile
        rasterfile_ndvi_name = rasterfile_red_name.replace('B04', 'NDVI')
        
        # Open Red band en schrijf data naar array
        rasterfile_red = gdal.Open(rasterfile_red_name, gdalconst.GA_ReadOnly )
        rasterband_red = rasterfile_red.GetRasterBand(1)
        array_red      = gdalnumeric.BandReadAsArray(rasterband_red)
        
        # Open NIR band en schrijf data naar array
        rasterfile_nir = gdal.Open(rasterfile_nir_name, gdalconst.GA_ReadOnly )
        rasterband_nir = rasterfile_nir.GetRasterBand(1)
        array_nir      = gdalnumeric.BandReadAsArray(rasterband_nir)
        
        # Bereken NDVI: Let op: Maak er eerst een array met floats van omdat resultaat een float is
        array_ndvi = (array_nir.astype(float) - array_red.astype(float))/(array_nir.astype(float) + array_red.astype(float))
        
        # Haal driver op voor output GeoTIFF raster bestand 
        driver = gdal.GetDriverByName("GTiff")
    
        # Haal aantal rijen en kolommen op voor output raster bestand
        nr_of_columns = rasterfile_red.RasterXSize
        nr_of_rows    = rasterfile_red.RasterYSize
        
        # Maak leeg raster bestand met datatype float32
        rasterfile_ndvi = driver.Create(rasterfile_ndvi_name, nr_of_columns, nr_of_rows, 1, gdal.GDT_Float32)

        # Kopieer geotrans en coordinaatsysteem
        gdalnumeric.CopyDatasetInfo(rasterfile_red, rasterfile_ndvi)

        # Haal band op en schrijf array naar band
        rasterband_ndvi = rasterfile_ndvi.GetRasterBand(1)
        gdalnumeric.BandWriteArray(rasterband_ndvi, array_ndvi)

        # Sluiten van bestanden
        array_red = None
        rasterfile_red  = None  
        array_nir = None
        rasterfile_nir  = None
        array_ndvi = None
        rasterfile_ndvi = None

        # Return name of NDVI file
        return rasterfile_ndvi_name

    except Exception as e: 
        
        try:
            rasterfile_red = None
            rasterfile_nir = None
            rasterfile_ndvi = None
        except:
            None

        print('Error function transform_raster_image')
        print(e)
