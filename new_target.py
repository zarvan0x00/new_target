
import requests
import json
import os
from discordwebhook import Discord



# Function to get the new targets
def get_new_targets():
    data = requests.get('https://raw.githubusercontent.com/arkadiyt/bounty-targets-data/main/data/yeswehack_data.json').json()
    result = set()
    for item in data:
        for target in item['targets']['in_scope']:
            if target['type'] == 'web-application':
                result.add(target['target'])
    return result

# Check if new_target.txt file exists
if os.path.isfile('new_target.txt') == False:
    # If file doesn't exist, create it and write the new targets to it
    with open('new_target.txt', 'w') as f:
        new_targets = get_new_targets()
        f.write('\n'.join(new_targets))
    print('Created new_target.txt file')
    exit()

# Read the old targets from new_target.txt file
with open('new_target.txt', 'r') as f:
    old_targets = set(f.read().splitlines())

# Get the new targets from the URL
new_targets = get_new_targets()

# Find the difference between old and new targets
difference = new_targets - old_targets

# Print the difference
if len(difference) > 0:
    print('New targets found:')
    print('\n'.join(difference))
    discord = Discord(url="https://discord.com/api/webhooks/1079056231999742034/M6YqM_BrZwVnHegRtJk2LKjuMboQeqoU2h7H-DIUkRiA66fMufI3SdcJ0JOEEQBCylZZ")
    discord.post(content='\n'.join(difference))

else:
    print('No new targets found')
    
# Update the new_target.txt file with the new targets
with open('new_target.txt', 'w') as f:
    f.write('\n'.join(new_targets))
