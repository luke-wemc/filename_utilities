
# coding: utf-8

# some utility functions to check filename structure meets DMP specifications.
# need to add some more rigorous checking functions to this, feel free to contribute!
# luke.sanger@wemcouncil.org

# import json library
import json
# import collections - for ordered dictionary
import collections

# load c3s_energy lookup table (json) as a dictionary + ordereddict
with open('/Users/user/Documents/ERA5/luke_scripts/filename_example/c3s_energy_lookup.json') as c3s_json:    
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
                if key in flist[i] and len(key) == el_info['length'] and el_info['pos'] == i\
                or el_info['pos'] == 8 and i == 8 and len(key) == el_info['length']\
                and int(word[1:5]) > 1950 and int(word[1:5]) < 3000\
                or el_info['pos'] == 9 and i == 9 and len(key) == el_info['length']\
                and int(word[1:5]) > 1950 and int(word[1:5]) < 3000:
                    print(key + " " + u'\u2713')
                    x = x + 1
    if x == 20:
        print("There are " + str(x) + " of 20 required elements in the filename ")
    elif x != 20 :
        print("There are " + color.RED + str(x) + color.END + " of 20 required elements in the filename")            


# print c3s_energy filename structure to terminal for reference
# print_structure()

# print c3s_energy filename elements to terminal for reference
# print_elements()

# filename string for testing
# fname = "H_ERA5_ECMW_T639_GHI_0000m_Euro_025d_S200001010000_E200001012300_ACC_MAP_01h_NA-_noc_org_NA_NA---_NA---_NA---.nc"

# check filename string against DMP guidelines
# call this to check integrity of input or output filenames
# first define fname as the string of your filename
# check_filename(fname)

