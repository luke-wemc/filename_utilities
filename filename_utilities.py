# some utility functions to check filename structure meets DMP specifications.
# luke.sanger@wemcouncil.org

# import json library
import json
# import collections - for ordered dictionary
import collections
# import datetime for metadata
import datetime
now = datetime.datetime.now()

# load c3s_energy lookup table (json) as a dictionary + ordereddict
with open('/data/private/resources/lookup/c3s_energy_lookup.json') as c3s_json:    
    c3s = json.load(c3s_json)
    c3s2 = collections.OrderedDict(c3s)

#######################
## utility functions ##
#######################

# set some colours for printing to terminal
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# function to print c3s_energy filename structure
def print_structure():
    s = ""
    for k in c3s2.keys():
        s += "<" + color.BOLD + k + color.END + ">_"    
    print(s[:-1] +".nc")
    
# function to print c3s_energy filename elements
def print_elements():
    for el_id, el_info in c3s.items():
        print(color.CYAN + el_id + color.END+ ':')
        for key in el_info:
            print(key + ':' , el_info[key])

# function to check a filename meets the DMP guidelines
def check_filename(fname):
    flist = fname.split('_')
    x = 0
    for i, word in enumerate(flist):
        for el_id, el_info in c3s.items():
            for key in el_info:
                if key in flist[i] and len(key) == el_info['length'] and el_info['pos'] == i                or el_info['pos'] == 8 and i == 8 and len(key) == el_info['length']                and int(word[1:5]) > 1950 and int(word[1:5]) < 3000                or el_info['pos'] == 9 and i == 9 and len(key) == el_info['length']                and int(word[1:5]) > 1950 and int(word[1:5]) < 3000:
                    print(key + " " + u'\u2713')
                    x = x + 1
    if x == 20:
        print("There are " + str(x) + " of 20 required elements in the filename ")
    elif x != 20 :
        print("There are " + color.RED + str(x) + color.END + " of 20 required elements in the filename")            

# function to create metadata from filename and lookup table
def mdata(fname):
    flist = fname.split('_')
    x = 0
    mdate = now.strftime("%Y-%m-%d")
    if '.nc' in fname:
        mtype = 'NetCDF'
    if '.csv' in fname:
        mtype = 'CSV'
    for i, word in enumerate(flist):
        for el_id, el_info in c3s.items():
            for key in el_info:
                if key in flist[i] and el_id == 'variable':
                    mtitle = el_info[key]
                if key in flist[i] and el_id == 'generation':
                    mabstract = el_info[key]
                if el_info['pos'] == 8 and i == 8 and len(key) == el_info['length']                and int(word[1:5]) > 1950 and int(word[1:5]) < 3000:
                    msedit = word.lstrip("S")
                    msdate = msedit[0:4] + '-' + msedit[4:6] + '-' + msedit[6:8] + '-' + msedit[8:]
                if el_info['pos'] == 9 and i == 9 and len(key) == el_info['length']                and int(word[1:5]) > 1950 and int(word[1:5]) < 3000:
                    meedit = word.lstrip("E")
                    medate = meedit[0:4] + '-' + meedit[4:6] + '-' + meedit[6:8] + '-' + meedit[8:]
                if key in flist[i] and el_id == 'temporal_resolution':
                    mtres = el_info[key]
                if key in flist[i] and el_id == 'spacial_resolution':
                    msres = el_info[key]
                    if mtitle == 'Air Temperature':
                        munit = 'K'
                    elif mtitle == 'Total Precipitation':
                        munit = 'm'
                    elif mtitle == 'Global Horizontal Irradiance':
                        munit = 'J m-2'
                    elif mtitle == 'Mean Sea Level Pressure':
                        munit = 'Pa'
                    elif mtitle == 'Wind Speed':
                        munit = 'm s-1'
                    elif mtitle == 'Evaporation':
                        munit = 'm of water equivalent'
                    elif mtitle == 'Snow Depth':
                        munit = 'm of water equivalent'
                    elif mtitle == 'Electricity Demand':
                        munit = 'W'
                    elif mtitle == 'Hydropower (Reservoir)':
                        munit = 'W'
                    elif mtitle == 'Hydropower (Run Of River)':
                        munit = 'W'
                    elif mtitle == 'Wind Power Onshore':
                        munit = 'W'
                    elif mtitle == 'Wind Power Offshore':
                        munit = 'W'
                    elif mtitle == 'Wind':
                        munit = 'W'
                    elif mtitle == 'Solar PV Power':
                        munit = 'W'
                x = x + 1
    metadata = '# General' + '\n## Title' + '\n### ' + mtitle + '\n## Abstract' + '\n### ' + mabstract    + '\n## Date' + '\n### ' + mdate + '\n## Date type' + '\n### Publication: Date identifies when the data was issued'    + '\n## Unit' + '\n### ' + munit + '\n## URL' + '\n### https://cds.climate.copernicus.eu/' + '\n## Data format'    + '\n### ' + mtype + '\n## Keywords' + '\n### ERA5, reanalysis, Copernicus, C3S, C3S Energy, WEMC'    + '\n## Point of contact' + '\n### Individual name' + '\n#### Alberto Troccoli' + '\n### Electronic mail address'    + '\n#### info@wemcouncil.org' + '\n### Organisation name' + '\n#### World Energy & Meteorology Council' + '\n### Role'    + '\n#### Owner: Party that owns the resource' + '\n# Usage' + '\n## Access constraints'    + '\n### Intellectual property rights: The IP of these data belongs to the EU Copernicus programme' + '\n## Use constraints'    + '\n### Creative Commons' + '\n## Citation(s)' + '\n### NA' + '\n## Temporal extent' + '\n## Begin date' + '\n### ' + msdate    + '\n## End date' + '\n### ' + medate + '\n## Temporal resolution' + '\n### ' + mtres + '\n## Geographic bounding box'    + '\n### westBoundLongitude -22.00' + '\n### eastBoundLongitude 45.00' + '\n### southBoundLatitude 27.00'    + '\n### northBoundLatitude 72.00' + '\n## Spatial resolution' + '\n### ' + msres + '\n# Lineage Statement'    + '\n## Original Data Source' + '\n## Statement'    + '\n### The original data sources are ECMWF ERA5 Reanalysis (available at: https://cds.climate.copernicus.eu)'    + '\n#'    + '\nDate'    # print(metadata)
    return(metadata)

# function to check filesize against expected from filename elements (x * y * t)
def fsize(fname):
    cubelist = iris.load(fname)
    cube = cubelist[0]
    # x,y,t (result = lat * lon * time)
    cubesize = cube.shape[0] * cube.shape[1] * cube.shape[2]
    # double result for 16bit precision (use *4 for 32bit precision)
    cubesize = cubesize * 2
    flist = fname.split('_')
    for i, word in enumerate(flist):
        for el_id, el_info in c3s.items():
            # get domain from filename and set lat lon int variables 
            if el_info['pos'] == 6 and word == 'Euro':
                lat = 185
                lon = 271  
            for key in el_info:
                # get start date from filename
                if el_info['pos'] == 8 and i == 8 and len(key) == el_info['length']\
                and int(word[1:5]) > 1950 and int(word[1:5]) < 3000:
                    msedit = word.lstrip("S")
                    msyear = msedit[0:4] 
                    msmonth = msedit[4:6] 
                    msday = msedit[6:8] 
                    mshour = msedit[8:]
                    msdate = msyear + '/' + msmonth + '/' + msday + ' ' + mshour
                # get end date from filename
                if el_info['pos'] == 9 and i == 9 and len(key) == el_info['length']\
                and int(word[1:5]) > 1950 and int(word[1:5]) < 3000:
                    meedit = word.lstrip("E")
                    medate = []
                    meyear = meedit[0:4] 
                    memonth = meedit[4:6] 
                    meday = meedit[6:8] 
                    mehour = meedit[8:]
                    medate = meyear + '/' + memonth + '/' + meday + ' ' + mehour
                    # identify start and end date as datetime objects
                    fstart = datetime.datetime.strptime(msdate, "%Y/%m/%d %H%M")
                    fend = datetime.datetime.strptime(medate, "%Y/%m/%d %H%M")
            if el_info['pos'] == 12 and word == '01h':
                dif = fend - fstart
                dif = dif.total_seconds() / 3600 + 1
                filsize = lat * lon * dif * 2
            if el_info['pos'] == 12 and word == '03h':
                dif = fend - fstart
                dif = dif.total_seconds() / 3600 + 1
                dif = dif / 3
                filsize = lat * lon * dif * 2
            if el_info['pos'] == 12 and word == '06h':
                dif = fend - fstart
                dif = dif.total_seconds() / 3600 + 1
                dif = dif / 6
                filsize = lat * lon * dif * 2
            if el_info['pos'] == 12 and word == '01d':
                dif = fend - fstart
                dif = dif.total_seconds() / 3600 + 1
                dif = dif / 24
                filsize = lat * lon * dif * 2
    if cubesize >= filsize:
        print('netcdf is expected size')
    elif cubesize < filsize:
        print('netcdf is too small! -> ' + str(cubesize) + ' bytes' + '\nexpected size at least -> ' + str(filsize) + ' bytes')  

