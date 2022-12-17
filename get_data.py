import urllib.parse, urllib.request, urllib.error, json, random, logging

#--------------------Important Constants and variables-----------------#
# num of indexes in the Json Dictionary
Num_Json_Indexes=50
# boolean determining if the local json file should be updated
updateJson = False
#-----------------------------------------------------------------------#

def pretty(obj):
    return json.dumps(obj, sort_keys = True, indent=2)

baseurl = "https://data.seattle.gov/resource/tazs-3rd5.json"

def get_crime_data(limit,offset):
    site_name = baseurl+'?$limit=' + str(limit) +'&$offset=' + str(offset)
    header = {'User-Agent':"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)\
         Chrome/107.0.0.0 Safari/537.36"}
    data_request = urllib.request.Request(site_name, headers=header)
    data_response = urllib.request.urlopen(data_request).read()
    crime_data = json.loads(data_response)
    return crime_data

def safe_get_crime_data(limit, offset):
    try:
        return get_crime_data(limit, offset)
    except urllib.error.HTTPError as e:
        print('Error trying to get your card:', str(e))

# Creates a Json string that accumulates all of the data via paging
# only run when data needs to updated
if updateJson == True:
    crimes_list = []

    print("Constructing file")
    for i in range(Num_Json_Indexes):
        sub_list = safe_get_crime_data(limit=10000, offset=i*10000)
        crimes_list.append(sub_list)

    with open("crimes_2008_present.json", "w") as file:
        file.write(pretty((crimes_list)))

    print("finished creating dictionary file")

crimes_2008_present = json.load(open('crimes_2008_present_raw.json', 'r', encoding='utf-8'))

print("stripping data")
stripped_list = []

for index in range(Num_Json_Indexes):
    if len(stripped_list) <= 170000:
        for report in crimes_2008_present[index]:
            stripped_list.append({
            "report_number": report["report_number"],
                "offense_parent_group": report["offense_parent_group"],
                "mcpp": report["mcpp"]
            })

# for index in range(Num_Json_Indexes):
#     for report in crimes_2008_present[index]:
#         stripped_list.append({
#         "report_number": report["report_number"],
#             "offense_parent_group": report["offense_parent_group"],
#             "mcpp": report["mcpp"]
#             })

with open("stripped_data.json", "w") as f:
    f.write(pretty(stripped_list))

print("finished")

# <To-Do> find coords for each of the MCPPS and police stations and put them on the map

# getting coordinates for mcpps
def generate_List(a, m):
    result = []
    for index in range(Num_Json_Indexes):
        for report in crimes_2008_present[index]:
            if a in report and report[a] not in result:
                result.append(report[a])
    return result

# These lists are primarily just for reference and for development purposes
#--------------------------------------------------------------------#
offense_parent_group = generate_List("offense_parent_group", crimes_2008_present)
# print(str(len(offense_parent_group)))
offenses = generate_List("offense", crimes_2008_present)  
mcpps = generate_List("mcpp", crimes_2008_present)
# print(str(mcpps))
#--------------------------------------------------------------------#
# print("Gettiing mcpp Coordinates")
mcpp_coordinates = {}

# for mcpp in mcpps:
#     for index in range(Num_Json_Indexes):
#         for report in crimes_2008_present[index]:
#             if "mcpp" in report:
#                 if report["mcpp"] == mcpp and "latitude" in report and "longitude" in report:
#                     mcpp_coordinates[mcpp] = { "lat": float(report["latitude"]), "lng": float(report["longitude"])}

# with open('mcpp_coordinates.json', "w") as file:
#     file.write(pretty(mcpp_coordinates))
# print("Finished")