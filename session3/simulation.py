# Simulation code will go here -- run in gateway, scan for edge, oee namespaces and randomize the values
# This code should run on an expression tag that is resolving now() to provide the current datetime.  As the time changes, this script will run.  Change the tag group to update every 5 seconds

	# Import required Ignition libraries
	import random as py_random  # Avoid naming conflict by aliasing random
	import system.tag
	import system.util
	
	# Set the wasteSetpoint as a percentage likelihood (e.g., 0.02 = 2% chance)
	wasteSetpoint = 0.02
	
	# Starting point in the tag structure (parent path)
	parentPath = "[default]Enterprise/Dallas/Press"
	
	# Function to simulate tag values for a specific Edge namespace
	def simulate_edge_values(edgePath):
	    # Convert edgePath to string in case it is not
	    edgePathStr = str(edgePath)
	
	    # Paths to the tags under the Edge namespace
	    infeedPath = edgePathStr + "/Infeed"
	    outfeedPath = edgePathStr + "/Outfeed"
	    statePath = edgePathStr + "/State"
	    wastePath = edgePathStr + "/Waste"
	
	    # Check if the tags exist
	    tagPaths = [infeedPath, outfeedPath, statePath, wastePath]
	    tagResults = system.tag.readBlocking(tagPaths)
	
	    # Verify that all tags are valid
	    if all([tag.quality.isGood() for tag in tagResults]):
	        infeedValue = tagResults[0].value
	        outfeedValue = tagResults[1].value
	        stateValue = tagResults[2].value
	        wasteValue = tagResults[3].value
	
	        # Simulate State: 90% chance of being 1 (machine running), 10% chance of being 0 (machine stopped)
	        stateValue = 1 if py_random.random() <= 0.9 else 0
	
	        # Only increment counters if the machine is running (State = 1)
	        if stateValue == 1:
	            # Increment Infeed
	            infeedValue += 1
	
	            # Determine if Waste should increment based on the wasteSetpoint
	            if py_random.random() <= wasteSetpoint:
	                # Increment Waste, Outfeed will not increment
	                wasteValue += 1
	            else:
	                # Increment Outfeed (but Outfeed cannot exceed Infeed)
	                outfeedValue = min(infeedValue, outfeedValue + 1)
	
	        # Write the new values back to the tags
	        system.tag.writeBlocking([
	            infeedPath,
	            outfeedPath,
	            statePath,
	            wastePath
	        ], [
	            infeedValue,
	            outfeedValue,
	            stateValue,
	            wasteValue
	        ])
	
	# Function to recursively browse tags starting from a given path and find Edge namespaces
	def browse_for_edge_namespaces(path):
	    # Get the direct children of the current path
	    results = system.tag.browse(path)
	
	    # Iterate through the results to find folders or Edge namespaces
	    for result in results.getResults():
	        # If the result is a folder, browse inside it recursively
	        if result['hasChildren']:
	            browse_for_edge_namespaces(result['fullPath'])
	        
	        # If an 'Edge' folder is found, run the simulation for this namespace
	        if result['name'] == 'Edge':
	            simulate_edge_values(result['fullPath'])
	
	# Function to simulate OEE values and write to tags
	def simulate_oee_values(oeePath):
	    # Convert oeePath to string in case it is not
	    oeePathStr = str(oeePath)
	
	    # Paths to the OEE tags under the OEE namespace
	    availabilityPath = oeePathStr + "/Availability"
	    qualityPath = oeePathStr + "/Quality"
	    performancePath = oeePathStr + "/Performance"
	
	    # Generate random OEE values between 0.60 and 0.72 (rounded to 2 decimal places)
	    availabilityValue = round(py_random.uniform(0.60, 0.72), 2)
	    qualityValue = round(py_random.uniform(0.60, 0.72), 2)
	    performanceValue = round(py_random.uniform(0.60, 0.72), 2)
	
	    # Write the values back to the tags
	    system.tag.writeBlocking([availabilityPath, qualityPath, performancePath],
	                             [availabilityValue, qualityValue, performanceValue])
	
	# Function to recursively browse tags starting from a given path and find OEE namespaces
	def browse_for_oee_namespaces(path):
	    # Get the direct children of the current path
	    results = system.tag.browse(path)
	
	    # Iterate through the results to find folders or OEE namespaces
	    for result in results.getResults():
	        # If the result is a folder, browse inside it recursively
	        if result['hasChildren']:
	            browse_for_oee_namespaces(result['fullPath'])
	
	        # If an 'OEE' folder is found, run the simulation for this namespace
	        if result['name'] == 'OEE':
	            simulate_oee_values(result['fullPath'])
	
	# Browse for all 'Edge' namespaces under the specified parentPath
	browse_for_edge_namespaces(parentPath)
	
	# Browse for all 'OEE' namespaces under the specified parentPath
	browse_for_oee_namespaces(parentPath)
