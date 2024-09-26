# Import required Ignition libraries
import system.tag
import json
import system.date

# Define the parent path for the Press namespace and BigQuery namespace
parentPath = "[default]Enterprise/Dallas/Press"
bigQueryBasePath = "[default]Enterprise/Dallas/BigQuery"
mqttTopicBase = "Enterprise/Dallas/BigQuery"

# Function to structure and write data for each press
def process_press(pressPath, pressName):
    # Define the BigQuery endpoint for the specific press
    endPointTag = bigQueryBasePath + "/EndPoint_" + pressName

    # Paths to the tag groups in the press namespace
    assetPath = pressPath + "/Asset"
    dashboardPath = pressPath + "/Dashboard/OEE"  # Correct path for OEE in Dashboard
    edgePath = pressPath + "/Edge"
    linePath = pressPath + "/Line"

    # Function to read tags and capture their values
    def read_tags(path, tag_names):
        return system.tag.readBlocking([path + "/" + tag_name for tag_name in tag_names])

    # Read all tags from each namespace
    assetTags = read_tags(assetPath, ["AssetID", "Name", "Model", "OEM"])
    dashboardTags = read_tags(dashboardPath, ["OEE", "Quality", "Performance", "Availability"])
    edgeTags = read_tags(edgePath, ["Infeed", "Outfeed", "State", "Waste"])
    lineTags = read_tags(linePath, ["Infeed", "Outfeed", "State", "Waste"])

    # Structure the data in a dictionary
    data = {
	    "timestamp": system.date.format(system.date.now(), "yyyy-MM-dd HH:mm:ss"),  # Format timestamp correctly
	    "Asset": {
	        "AssetID": assetTags[0].value,
	        "Name": assetTags[1].value,
	        "Model": assetTags[2].value,
	        "OEM": assetTags[3].value
	    },
	    "Dashboard": {
	        "OEE": dashboardTags[0].value,
	        "Quality": dashboardTags[1].value,
	        "Performance": dashboardTags[2].value,
	        "Availability": dashboardTags[3].value
	    },
	    "Edge": {
	        "Infeed": edgeTags[0].value,
	        "Outfeed": edgeTags[1].value,
	        "State": edgeTags[2].value,
	        "Waste": edgeTags[3].value
	    },
	    "Line": {
	        "Infeed": lineTags[0].value,
	        "Outfeed": lineTags[1].value,
	        "State": lineTags[2].value,
	        "Waste": lineTags[3].value
	    }
	}

    # Convert the structured data to a JSON string
    json_data = json.dumps(data)

    # Write the structured JSON data to the specific press's BigQuery endpoint tag
    system.tag.writeBlocking([endPointTag], [json_data])

    # Publish to MQTT
    mqtt_topic = "{}/EndPoint_{}".format(mqttTopicBase, pressName)
    system.cirruslink.engine.publish("EMQX", mqtt_topic, json_data.encode("utf-8"), 0, 0)

# Function to browse and process all presses dynamically
def browse_and_process_presses(path):
    # Browse the parent path to find all presses
    results = system.tag.browse(path)

    for result in results.getResults():
        if result['hasChildren']:
            pressPath = str(result['fullPath'])
            pressName = result['name']
            process_press(pressPath, pressName)

# Browse and process all presses under the specified parentPath
browse_and_process_presses(parentPath)
