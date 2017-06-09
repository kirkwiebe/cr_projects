from hudlie import Hudlie
import random
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# get Google sheets
def getGoogleSheet(docname, sheetname):
    scope = ['https://spreadsheets.google.com/feeds']
    credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    gc = gspread.authorize(credentials)
    doc = gc.open(docname)
    sheet = doc.worksheet(sheetname)
    return sheet

lookup_table = getGoogleSheet('Support DA Lookup Table', 'DA_Availability')
temp_schedule = getGoogleSheet('2017 Spring/Summer Schedule', 'Roster')


# get lookup_table information
lookup_records = lookup_table.get_all_records()
list_of_hudlies = []
first_shift = []
second_shift = []
third_shift = []
fourth_shift = []

for rep in lookup_records:
    hudlie = Hudlie(**rep)
    list_of_hudlies.append(hudlie)


for hudlie in list_of_hudlies:
    if hudlie.shift_start == 7:
        first_shift.append(hudlie.full_name)
    elif hudlie.shift_start == 8:
        second_shift.append(hudlie.full_name)
    elif hudlie.shift_start == 9:
        third_shift.append(hudlie.full_name)
    elif hudlie.shift_start == 10:
        fourth_shift.append(hudlie.full_name)

# get cell ranges
first_shift_roster = temp_schedule.range('D2:D20')
second_shift_roster = temp_schedule.range('E2:E20')
third_shift_roster = temp_schedule.range('F2:F20')
fourth_shift_roster = temp_schedule.range('G2:G20')

# function to write to cell ranges 
def create_roster(cell_range, list):

    for cell in cell_range:
        if len(list) > 0:
            cell.value = random.choice(list)
            list.remove(cell.value)
        else:
            continue

    temp_schedule.update_cells(cell_range)

create_roster(first_shift_roster, first_shift)
create_roster(second_shift_roster, second_shift)
create_roster(third_shift_roster, third_shift)
create_roster(fourth_shift_roster, fourth_shift)
