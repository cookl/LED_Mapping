import json

#an example script to read out LED mapping from the json created by makeMappingJson.py

def get_led_from_entry(mPMT_dict, led_ch):
    #return information in dictionary
    led_info ={}
    led_info["position_id"] = mPMT_dict["led"+str(led_ch)+"_pos_id"]
    led_info["col_type"] = mPMT_dict["led"+str(led_ch)+"_col_type"]
    led_info["wavelength"] = mPMT_dict["led"+str(led_ch)+"_wl"]
    
    return led_info

def get_key_slot_id(json_data, slot_id):
    for key, value in json_data.items():
        if value["slot_id"] == slot_id:
            return key
    return None  # Return None if no match is found    

# Open and read the JSON file
with open('led_mapping.json', 'r') as file:
    led_data = json.load(file)
    
#example 1 get info on a specific led channel(raw data format) from a mPMT card ID (raw data format)
card_id = 104 
led_channel = 1 #1,2 or 3

led_info = get_led_from_entry(led_data[str(card_id)], led_channel)
print("mPMT with card id",card_id,"led channel",led_channel)
print(led_info)


#example 2 get info on a specific led channel(raw data format) from a mPMT slot id
slot_id = 57
led_channel = 3 #1,2 or 3

card_id = get_key_slot_id(led_data,slot_id) 
led_info = get_led_from_entry(led_data[str(card_id)], led_channel)
print("mPMT with slot id",slot_id,"led channel",led_channel)
print(led_info)

    