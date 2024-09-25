import json
import requests

def getLEDfromModulo(mpmtin):
    #submit curl request to modulo
    url ="https://modulo.triumf.ca/api/v2/mpmts/leds?MPMTIN(s)="+mpmtin
    try:
        response = requests.get(url)  # Send GET request to the URL
        response.raise_for_status()   # Check if the request was successful (status code 200)
        json_data = response.json()   # Parse the response as JSON
        return json_data
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
    except ValueError:
        print("Failed to parse JSON.")
    return None

# Open and read the JSON file for mPMT slots
with open('modulo_dump.json', 'r') as file:
    data = json.load(file)

#make a list of all the mPMTs for modulo
mPMT_list = []
MPMTIN_slot_id_mapping = {}
for mPMT in data["data"]:
    # print(mPMT)
    mpmtin = mPMT["MPMTIN"]
    if mpmtin is not None:
        mPMT_list.append(mpmtin)
        slot_id = mPMT["slot_id"]
        MPMTIN_slot_id_mapping[mpmtin]=slot_id
        
mPMT_list_str = ",".join(mPMT_list)

led_data = getLEDfromModulo(mPMT_list_str)

#create a dictionary fot the led information
out_led_mapping = {}

for mPMT in led_data["data"]:    
    mpmtin = mPMT["MPMTIN"]
    slot_id = MPMTIN_slot_id_mapping[mpmtin]

    parts = mpmtin.split('-')
    card_id = int(parts[-1])  # Get the last part

    led1_col_type = mPMT["led1_470nm_collimator_type"]
    led2_col_type = mPMT["led2_405nm_collimator_type"]
    led3_col_type = mPMT["led3_365nm_collimator_type"]
  
    led1_pos_id = mPMT["led1_470nm_coord_id"]
    led2_pos_id = mPMT["led2_405nm_coord_id"]
    led3_pos_id = mPMT["led3_365nm_coord_id"]
    
    led1_wl = 470
    led2_wl = 405
    led3_wl = 365
    
    mPMT_mapping_dict = {}
    mPMT_mapping_dict["MPMTIN"]=mpmtin
    mPMT_mapping_dict["slot_id"]=slot_id
    mPMT_mapping_dict["led1_col_type"]=led1_col_type
    mPMT_mapping_dict["led2_col_type"]=led2_col_type
    mPMT_mapping_dict["led3_col_type"]=led3_col_type
    
    mPMT_mapping_dict["led1_pos_id"]=led1_pos_id
    mPMT_mapping_dict["led2_pos_id"]=led2_pos_id
    mPMT_mapping_dict["led3_pos_id"]=led3_pos_id    

    mPMT_mapping_dict["led1_wl"]=led1_wl
    mPMT_mapping_dict["led2_wl"]=led2_wl
    mPMT_mapping_dict["led3_wl"]=led3_wl
    
    out_led_mapping[card_id]= mPMT_mapping_dict

outputMapping_json = json.dumps(out_led_mapping, indent=2)
with open('../led_mapping.json', 'w') as file:
    file.write(outputMapping_json)    
           
