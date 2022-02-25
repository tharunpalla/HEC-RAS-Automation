from mil.army.usace.hec.vortex.convert import GridToPointConverter
from mil.army.usace.hec.vortex import Options
from mil.army.usace.hec.vortex.io import DataReader
from glob import glob
from java.nio.file import Paths

#DSS Grid Files to convert to time series
d_files = glob("C:\Users\chand\Downloads\HEC_DSS_Automation\GribToPoint\est_output.dss")

#Output DSS File
output_dss = Paths.get("C:\Users\chand\Downloads\HEC_DSS_Automation\GribToPoint\st_output_grib2point1.dss")

#Shapefile
clip_shp = Paths.get("C:\Users\chand\Downloads\HEC_DSS_Automation\Vortex\examples\src\main\jython\Basin Shapefile\Basins.shp")

#Shapefile attribute for zonal statistics
name = 'Name'

#Output DSS file path partA
basin = '*'
ds = 'UA_sanitized'

#Loop through each dss file
for dss_file in d_files:

    #Get dss pathnames
    sourceGrids = DataReader.getVariables(dss_file)

    #Output DSS wite options
    write_options = Options.create()
    write_options.add('partF', ds )
    write_options.add('partA', 'SHG')
    write_options.add('partB', basin)

    #Convert the Data
    myImport = GridToPointConverter.builder()\
            .pathToGrids(dss_file)\
            .variables(sourceGrids)\
            .pathToFeatures(clip_shp)\
            .field(name)\
            .destination(output_dss)\
            .writeOptions(write_options).build()
    myImport.convert()
