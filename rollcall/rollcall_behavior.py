# import libraries/obtain credentials
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']
credentials = ServiceAccountCredentials.from_json_keyfile_name('rollcall_creds.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open_by_url("https://docs.google.com/spreadsheets/d/1UuD0q08bbdMjnJrb85Uwfbb46SCJWIWkHi1JH-9QA_0/edit#gid=1528692932")
worksheet = wks.get_worksheet(6)

# set cell lists for shifts
SEVENAM_SHIFT = ['D6', 'D7', 'D8', 'D9', 'D10', 'D11', 'D12', 'D13', 'D14', 'D15', 'D16']
EIGHT_SHIFT = ['D17', 'D18', 'D19', 'D20', 'D21', 'D22', 'D23', 'D24', 'D25', 'D26', 'D27']
NINE_SHIFT = ['D28', 'D29', 'D30', 'D31', 'D32', 'D33', 'D34', 'D35', 'D36', 'D37', 'D38']
TEN_SHIFT = ['D39', 'D40', 'D41', 'D42', 'D43', 'D44', 'D45', 'D46', 'D47', 'D48', 'D49']

# set cell lists for breaks
TEN_BREAK = ['H6', 'H7', 'H8', 'H9', 'H10', 'H11', 'H12']
ELEVEN_BREAK = ['H13', 'H14', 'H15', 'H16', 'H17', 'H18', 'H19']
TWELVE_BREAK = ['H20', 'H21', 'H22', 'H23', 'H24', 'H25', 'H26']
ONE_BREAK = ['H27', 'H28', 'H29', 'H30', 'H31', 'H32', 'H33']
TWO_BREAK = ['H34', 'H35', 'H36', 'H37', 'H38', 'H39', 'H40', 'H41']
THREE_BREAK = ['H42', 'H43', 'H44', 'H45', 'H46', 'H47', 'H48', 'H49']

# get list of names for the day
def get_all_names():

    worksheet = wks.get_worksheet(6)
    values_list = worksheet.col_values(4)
    get_all_names.names_list = []
    for value in values_list:
        if value == '':
            continue
        else:
            get_all_names.names_list.append(value)

    return get_all_names.names_list

# create function to remove names from list
def remove_names(list, names):
    for item in list:
        if worksheet.acell(item).value != '' and worksheet.acell(item).value in names:
            names.remove(worksheet.acell(item).value)
        else:
            continue

# function that gets current time and adjusts that list
def get_current_shifts(names):
    # set current time
    current_time = datetime.datetime.now()

    # sets available hours
    if current_time.hour >= 7 and current_time.hour < 23:
        # 7am
#        if current_time.hour == 7:
#            remove_names(EIGHT_SHIFT, names)
#            remove_names(NINE_SHIFT, names)
#            remove_names(TEN_SHIFT, names)
#            get_current_shifts.answer = names
#            return get_current_shifts.answer
        # 8am
        if current_time.hour == 8:
            remove_names(NINE_SHIFT, names)
            remove_names(TEN_SHIFT, names)
            get_current_shifts.answer = names
            return get_current_shifts.answer
        # 9am
        elif current_time.hour == 9:
            remove_names(TEN_SHIFT, names)
            get_current_shifts.answer = names
            return get_current_shifts.answer
        # 10am
        elif current_time.hour == 10:
            remove_names(TEN_BREAK, names)
            get_current_shifts.answer = names
            return get_current_shifts.answer
        # 11am
        elif current_time.hour == 11:
            remove_names(ELEVEN_BREAK, names)
            get_current_shifts.answer = names
            return get_current_shifts.answer
        # 12pm
        elif current_time.hour == 12:
            remove_names(TWELVE_BREAK, names)
            get_current_shifts.answer = names
            return get_current_shifts.answer
        # 1pm
        elif current_time.hour == 13:
            remove_names(ONE_BREAK, names)
            get_current_shifts.answer = names
            return get_current_shifts.answer
        # 2pm
        elif current_time.hour == 14:
            remove_names(TWO_BREAK, names)
            get_current_shifts.answer = names
            return get_current_shifts.answer
        # 3pm
        elif current_time.hour == 15:
            remove_names(THREE_BREAK, names)
            get_current_shifts.answer = names
            return get_current_shifts.answer
        # 4pm
        elif current_time.hour == 16:
            remove_names(SEVENAM_SHIFT, names)
            get_current_shifts.answer = names
            return get_current_shifts.answer
        # 5pm
        elif current_time.hour == 17:
            remove_names(SEVENAM_SHIFT, names)
            remove_names(EIGHT_SHIFT, names)
            get_current_shifts.answer = names
            return get_current_shifts.answer
        # 6pm
#        elif current_time.hour == 18:
#            remove_names(SEVENAM_SHIFT, names)
#            remove_names(EIGHT_SHIFT, names)
#            remove_names(NINE_SHIFT, names)
#            get_current_shifts.answer = names
#           return get_current_shifts.answer
    else:
        get_current_shifts.answer = "Please rollcall during business hours."
        return get_current_shifts.answer
    # return names


#get_all_names()
#input_list = get_all_names.names_list
#get_current_shifts(input_list)
# function that takes that list and checks it against break times
