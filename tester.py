# FOR THE GRADER: In order to access the JSON set updateJson = True
# The json file was too big in order to push to github so i didn't upload
# it. Pleasw let me know if the json takes to long to load so I can show 
# you using a local JSON file on my computer


from flask import Flask, render_template, request   
import urllib.parse, urllib.request, urllib.error, json, random, logging

# Primary Json Dictionary 
crimes_2008_present = json.load(open('stripped_data.json', 'r', encoding='utf-8'))

# Description: returns a list of the distinct values that a key in
#  the Json can have 

def generate_List(a, m):
    result = []
    for report in crimes_2008_present:
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


# Description: If the user can choose a starting year and 
# ending year in order to filter data. If the starting year and ending 
# year are the same then it will show only the results from that year
# Paramters: 
#   start_year - the minimum year to include in search 
#   end_year - the maximum year to include in search 
# Return: Boolean
# Note: implement a notion 
def filter_by_year(curr_year, start_year=2008, end_year=2020):
        if start_year == end_year:
            return curr_year == start_year
        else:
            return (curr_year >= start_year and curr_year <= end_year)

# <TO-DO>
# Description: Filters the data so that only results within specified 
# locations show up
# Paramters:
#   location: the location that you want to filter by
#   target_locations: locations(s) to filter for 
def filter_by_location(curr_location, target_locations):
    return(curr_location in target_locations)

# Sorts a map by its key valuee, with higher values at the top
# of the list
def create_rankings(map):
    sortedmap = sorted(map.items(), key=lambda x:x[1], reverse=True)
    return sortedmap

#--------------------Test for create_rankings------------------#
# print("==========testing create rankings=========== \n")
# print(str(create_rankings(testing_map)))
#--------------------------------------------------------------#



# <TO-DO>-<Make more efficient by sorting the crimetypes>
# <Note>-<this could be made more flexible by using the 
# Description: Creates and returns a map with all of the mcpp locations as the keys and  
# the number of incidents that that have happened at that locations that are 
# of the specified crimetype(s) as the values
# Parameters: 
#   crimetypes(List) - the type of crime that needs to be tallied up
#   filterTag(String) - "either offense_parent_group" or "offense"
#   start_year - the minimum year to include in search 
#   end_year - the maximum year to include in search 
# Return: Map
def map_locations_to_incident(crimetypes, locations_list=mcpps, filtertag = "offense_parent_group", start_year=2008, end_year=2020):
    if len(locations_list) == 0:
        locations_list = mcpps
    if len(crimetypes) == 0:
        crimetypes = offense_parent_group

    locations_to_incident = {}
    for report in crimes_2008_present:
        current_year = int(report["report_number"][0:4])
        if (filter_by_year(current_year, start_year, end_year) and "mcpp" in report):
                location = report["mcpp"]
                if location in locations_list:
                    if location not in locations_to_incident:
                        if report[filtertag] in crimetypes:
                                locations_to_incident[location] = 1
                    else:
                         if report[filtertag] in crimetypes:
                                locations_to_incident[location] += 1
    
    return locations_to_incident
#  Use control F on the json file and see if its accurate 
# map for testing 
# crime_types = ['DRIVING UNDER THE INFLUENCE', 'ROBBERY']
# testing_map = map_locations_to_incident(crime_types, mcpps,"offense_parent_group", 2008, 2020)
# testing_map = create_rankings(testing_map)
#--------------------Test for map_locations_to_incident------------------#
# print("\n=========testing map_locations_to_incident======= \n")
# # print(str(testing_map))
#------------------------------------------------------------------------#

# Description: returns most common offenses for a specified set of locations
# Parameters:
#    locations_list - list of locations you want to search for 
def most_common_crimes_in_location(crimetypes, locations_list=mcpps, tag="offense_parent_group", start_year=2008, end_year=2020): 
    if len(locations_list) == 0:
        locations_list = mcpps
    if len(crimetypes) == 0:
        crimetypes = offense_parent_group

    crimes_to_amount = {}
    for report in crimes_2008_present:
        current_year = int(report["report_number"][0:4])
        if ("mcpp" in report and filter_by_year(current_year, start_year, end_year)):
            location = report['mcpp']
            crime_type = report[tag]
            # Checks if the locations of the report is one of the ones in locations_list 
            if location in locations_list:
                if crime_type not in crimes_to_amount:
                    crimes_to_amount[crime_type] = 1 
                else:
                    crimes_to_amount[crime_type] += 1
    return crimes_to_amount
                        
# locations_sample = ["MAGNOLIA"]
# test_list = most_common_crimes_in_location(offense_parent_group, locations_sample, "offense_parent_group", 2008, 2020)
# ranked_test_list = create_rankings(test_list)
# print("\n====================Testing most_crimes_in_location================\n")
# print(str(ranked_test_list))

# print("====================Testing Finished================")


# <TO-DO>
# Description: Finds all of the incident reports that have happened at a given lat and long
# over the given amount of time, the user can filter by types of crimes
# def find_reports_at_location(lat, long, crime_types, start_year=2008, end_year=2020):




# adds up the total number of incidents that have happened for the entire 
# city of Seattle
def get_total_incidents(map):
    total_incidents = 0
    for location in map:
        total_incidents += map.get(location)
    return total_incidents
#--------------------Test for get_total_incidents------------------#
# print("\nTotal number of incidents = " + str(get_total_incidents(testing_map)))
#------------------------------------------------------------------#



# <TO-DO>
# class representing an incident report, this will be used for representing each 
# of the incidents that have occured at a location specified by the user or at
# the user's current location 
# class incident_report():




#+++++++++++++++++++++++++++++++++++ Main Script+++++++++++++++++++++++++++++++++++++++#
mcpp_coord = {
  "ALASKA JUNCTION": {
    "lat": 47.56576334,
    "lng": -122.398843342
  },
  "ALKI": {
    "lat": 47.57697854,
    "lng": -122.414624116
  },
  "BALLARD NORTH": {
    "lat": 47.68047949,
    "lng": -122.375716926
  },
  "BALLARD SOUTH": {
    "lat": 47.67309049,
    "lng": -122.377546622
  },
  "BELLTOWN": {
    "lat": 47.61432034,
    "lng": -122.344143639
  },
  "BITTERLAKE": {
    "lat": 47.71694613,
    "lng": -122.362273005
  },
  "BRIGHTON/DUNLAP": {
    "lat": 47.53545842,
    "lng": -122.269980732
  },
  "CAPITOL HILL": {
    "lat": 47.61873954,
    "lng": -122.320854484
  },
  "CENTRAL AREA/SQUIRE PARK": {
    "lat": 47.610819366868995,
    "lng": -122.3176374777895
  },
  "CHINATOWN/INTERNATIONAL DISTRICT": {
    "lat": 47.59492265,
    "lng": -122.325967055
  },
  "CLAREMONT/RAINIER VISTA": {
    "lat": 47.56680754,
    "lng": -122.2924541
  }, 
  "COLUMBIA CITY": {
    "lat": 47.55342827,
    "lng": -122.281877855
  },
  "COMMERCIAL DUWAMISH": {
    "lat": 47.56630275,
    "lng": -122.353389551
  },
  "COMMERCIAL HARBOR ISLAND": {
    "lat": 47.57101267,
    "lng": -122.348423777
  },
  "DOWNTOWN COMMERCIAL": {
    "lat": 47.60965503,
    "lng": -122.333098112
  },
  "EASTLAKE - EAST": {
    "lat": 47.63714358,
    "lng": -122.322411073
  },
  "EASTLAKE - WEST": {
    "lat": 47.64914848,
    "lng": -122.324470013
  },
  "FAUNTLEROY SW": {
    "lat": 47.51702094,
    "lng": -122.379488201
  },
  "FIRST HILL": {
    "lat": 47.60620026,
    "lng": -122.316125606
  },
  "FREMONT": {
    "lat": 47.65674569,
    "lng": -122.342372301
  },
  "GENESEE": {
    "lat": 47.56125708,
    "lng": -122.284907852
  },
  "GEORGETOWN": {
    "lat": 47.56380429,
    "lng": -122.329368515
  },
  "GREENWOOD": {
    "lat": 47.69094123,
    "lng": -122.349916227
  },
  "HIGH POINT": {
    "lat": 47.54284447,
    "lng": -122.373033606
  },
  "HIGHLAND PARK": {
    "lat": 47.52178312,
    "lng": -122.335571292
  },
  "HILLMAN CITY": {
    "lat": 47.54787394,
    "lng": -122.283375792
  },
  "JUDKINS PARK/NORTH BEACON HILL": {
    "lat": 47.60032113,
    "lng": -122.302236384
  },
  "LAKEWOOD/SEWARD PARK": {
    "lat": 47.55035985,
    "lng": -122.260033567
  },
  "MADISON PARK": {
    "lat": 47.63802564,
    "lng": -122.277100743
  },
  "MADRONA/LESCHI": {
    "lat": 47.59618119,
    "lng": -122.289022197
  },
  "MAGNOLIA": {
    "lat": 47.64022597,
    "lng": -122.404363753
  },
  "MID BEACON HILL": {
    "lat": 47.5541858,
    "lng": -122.317183527
  },
  "MILLER PARK": {
    "lat": 47.62129036,
    "lng": -122.311370555
  },
  "MONTLAKE/PORTAGE BAY": {
    "lat": 47.6353896,
    "lng": -122.312715589
  },
  "MORGAN": {
    "lat": 47.52849122,
    "lng": -122.385363498
  },
  "MOUNT BAKER": {
    "lat": 47.57834034,
    "lng": -122.288726822
  },
  "NEW HOLLY": {
    "lat": 47.53704403,
    "lng": -122.28234489
  },
  "NORTH ADMIRAL": {
    "lat": 47.58473824,
    "lng": -122.390487322
  },
  "NORTH BEACON HILL": {
    "lat": 47.57835047,
    "lng": -122.299778401
  },
  "NORTH DELRIDGE": {
    "lat": 47.54102078,
    "lng": -122.359595869
  },
  "NORTHGATE": {
    "lat": 47.70858578,
    "lng": -122.321918379
  },
  "PHINNEY RIDGE": {
    "lat": 47.66870094,
    "lng": -122.357228821
  },
  "PIGEON POINT": {
    "lat": 47.56381274,
    "lng": -122.363337506
  },
  "PIONEER SQUARE": {
    "lat": 47.59999194,
    "lng": -122.330343467
  },
  "QUEEN ANNE": {
    "lat": 47.62501856,
    "lng": -122.35670596
  },
  "RAINIER BEACH": {
    "lat": 47.52240866,
    "lng": -122.264496402
  },
  "RAINIER VIEW": {
    "lat": 47.51070128,
    "lng": -122.272036428
  },
  "ROOSEVELT/RAVENNA": {
    "lat": 47.67577382,
    "lng": -122.301162906
  },
  "ROXHILL/WESTWOOD/ARBOR HEIGHTS": {
    "lat": 47.51086925632609,
    "lng": -122.38086143778638
  },
  "SANDPOINT": {
    "lat": 47.68074482,
    "lng": -122.263646939
  },
  "SLU/CASCADE": {
    "lat": 47.61495252,
    "lng": -122.335295373
  },
  "SODO": {
    "lat": 47.58042375,
    "lng": -122.321397369
  },
  "SOUTH BEACON HILL": {
    "lat": 47.53155081,
    "lng": -122.285043308
  },
  "SOUTH DELRIDGE": {
    "lat": 47.52233423,
    "lng": -122.359626596
  },
  "SOUTH PARK": {
    "lat": 47.52644854,
    "lng": -122.317581856
  },
  "UNIVERSITY": {
    "lat": 47.66700204,
    "lng": -122.304404341
  },
  "UNKNOWN": {
    "lat": 47.5403703,
    "lng": -122.368841395
  },
  "WALLINGFORD": {
    "lat": 47.66138609,
    "lng": -122.338860039
  }
}

# Runs the flask application
# <TO-DO>
# 1.) Allow the user to pick what year range that they want to filter for
# using a text box method, it probably inputs as a string so change to an int
# 2.) user input for what kinds of crimes they want to filter by using the
# check boxes

app = Flask(__name__)

@app.route("/")
def main_handler():
    app.logger.info("In MainHandler")
    return render_template('test_template.html', list=mcpps)

@app.route("/gresponse")
def list_output_handler():
    # start year
    start_year = int(request.args.get('start_year_in'))
    app.logger.info(start_year)
    # end year
    end_year = int(request.args.get('end_year_in'))
    app.logger.info(end_year)
    # crime types
    crime_types = request.args.getlist('crime_type') 
    app.logger.info(crime_types)
    # locations list 
    locations_list = request.args.getlist('mcpp')
    app.logger.info(locations_list)
    # user request
    user_request = request.args.get("user_request")
    app.logger.info(user_request)
 
    
    # print(str(ranked_list))
    if user_request == "locations_ranking":
        result_list = map_locations_to_incident(crime_types, locations_list,"offense_parent_group",\
         start_year, end_year)
        total_crimes = get_total_incidents(result_list)
        ranked_list = create_rankings(result_list)

        top_ten_list = ranked_list[:10]
        
        plot_list = []
       
        for location in top_ten_list:
            print(location[0])
            if location[0] in mcpp_coord:
                plot_list.append(mcpp_coord[location[0]])

        return render_template('orderedlist.html', list=ranked_list, total=total_crimes, plots = plot_list)
    else:
        # something is wrong with this method
        result_list = most_common_crimes_in_location(crime_types, locations_list,"offense_parent_group",\
         start_year, end_year)
        ranked_list = create_rankings(result_list)

        plot_list= []
        for location in locations_list:
            print(location[0])
            if location in mcpp_coord:
                plot_list.append(mcpp_coord[location])

        return render_template('most_common.html', list=ranked_list, plots=plot_list)
        
       
if __name__ == "__main__":
    app.run(host = "localhost", port=8080, debug=True)