
import gspread
from oauth2client.service_account import ServiceAccountCredentials

from datetime import datetime
import pytz

"""Code written by Asher Mouat"""

# Necessary credentials and sheet identification for authenticating
# and reading/writing
JSON_KEYFILE = 'Replace_This_Json.json'
SHEET_ID = 'add your own sheet ID'
scope = ['https://www.googleapis.com/auth/spreadsheets']

# Dictionary holding key-value pairs of serial number from button and action
# each button is assigned
buttons = {'XXXbuttonserialnumberXXX' : "User helped inside facility", 'XXXbuttonserialnumberXXX' : "User told to GTFO"}

def lambda_main(serial_number):

	# Get time stamp for when button was pressed
	# Check python's doc on pytz and datetime for more info
	utc_time = datetime.utcnow()
	eastern = pytz.timezone('US/Eastern')
	utc_time = utc_time.replace(tzinfo=pytz.UTC)
	time_stamp = utc_time.astimezone(eastern)

   # Authenticationm, made very easy by gspread: https://github.com/burnash/gspread
	credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEYFILE, scope)
	gc = gspread.authorize(credentials)

	# Accessing sheet object, which I believe is a 2D list
	gsheet = gc.open_by_key(SHEET_ID).sheet1

	# Basic list containing str representations of data
	col_time = gsheet.col_values(1)

	# Find next blank cell, remember coordinate of cell
	cell_coord = None
	for cell in range(len(col_time)):
		if (col_time[cell] == ''):
			cell_coord = 'A' + str(cell+1)
			break
	# Update relevant cells with necessary info
	gsheet.update_acell(cell_coord, time_stamp)

	action_cell_coord = 'B' + cell_coord[1]
	gsheet.update_acell(action_cell_coord, buttons[serial_number])

"""lambda_handler will activate when button is pressed. Button sends JSON payload that looks like
   {
    "serialNumber" : "ABCDEFG12345",
    "batteryVoltage" : "2000mV",
    "clickType" : "SINGLE"
   }
   Payload is indexed the same way as a python dictionary
"""
def lambda_handler(context, event):
	lambda_main(context['serialNumber'])
