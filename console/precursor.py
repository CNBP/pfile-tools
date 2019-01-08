# An illustration of the overall workflow:

from PythonUtil.env import load_dotenv_var
from PythonUtil.file import unique_name

IP = load_dotenv_var("scanner_IP")
username = load_dotenv_var("scanner_username")
password = load_dotenv_var("scanner_password")
path = load_dotenv_var("p_folder")

# Create he client.
from console.access import getSSHClient
from console.copy import download_through_client
SSH_client = getSSHClient(IP, username, password)

# Ask user for "DATE"
date = input("Please enter the DAY of the scan (e.g. 09, for 9th of this month). We assume it was done within the past few days as P data do not persist beyond that. ")

# Ask user for "MRN Number"
MRN = input("Please enter SEVEN digits MRN number of the patient. ")
assert 0 < int(MRN) < 9999999

# Login remotely.
stdin, output, stderr = SSH_client.exec_command(r"cd " + path + r"; ls P*.7 -lasth")

# Store errors in a variable.
errors = stderr.readlines()

# Store the output in a variable
ls_output = output.readlines()

# As the output are already sorted by time with the most recent at the top,
# First entry is a total. 2nd entry is the first real data point from LS command.
list_properties = ls_output[1].split(" ")

index_filename = 0
index_month = 0
index_time = 0
index_day = 0

# Determine the index of the variable.
for property in list_properties:


    # Continue if the property is blank.
    if property == "":
        continue

    # strip the trailing garbage
    property_stripped = property.rstrip()

    # If the property starts with P and end with 7*
    if property_stripped[0] == "P" and property_stripped[-1] == "*":
        # Determine the index of file name.
        index_filename = list_properties.index(property)
        index_time = index_filename - 1
        index_day = index_filename - 2
        index_month = index_filename - 3

if index_filename == 0:
    raise ValueError("No items in this list contain P files! Why are you doing this to me. I am quitting. ")

# Loop through the ls_output for date match:
for ls_row in ls_output:

    # Split into strings:
    list_properties = ls_row.split(" ")

    # If date is a match,
    if list_properties[index_day] == date:

        # Find out the proper name of the file to be downloaded with the matching date.
        file_name = list_properties[index_filename].rstrip()

        # Form the absolute path to the remote file. Linux style.
        path_remote_file = path + r"/" + file_name

        # Initiate the download request.
        download_through_client(SSH_client, path_remote_file, file_name.replace('*', "")+"_"+unique_name())

    # Check if MRN number matches.






# Parse date:

# Parse file name:




SSH_client.close()


# run ls -lasth

# ls P*.7 -lasth
# Top
# Example:
"""

{sdc@MHSJMR1}[106] ls P*.7 -lasth
 25M -rwxrwxrwx 1 sdc informix  25M Jan  8 09:27 P11776.7*
 25M -rwxrwxrwx 1 sdc informix  25M Jan  7 14:34 P23552.7*
 65M -rwxrwxrwx 1 sdc informix  65M Jan  4 09:48 P13312.7*
9.3M -rwxrwxrwx 1 sdc informix 9.3M Jan  2 14:02 P34304.7*
2.4M -rwxrwxrwx 1 sdc informix 2.4M Jan  2 13:58 P33280.7*
2.4M -rwxrwxrwx 1 sdc informix 2.4M Jan  2 13:32 P30720.7*
 25M -rwxrwxrwx 1 sdc informix  25M Dec 28 09:54 P10752.7*
 25M -rwxrwxrwx 1 sdc informix  25M Dec 21 14:37 P46592.7*
 25M -rwxrwxrwx 1 sdc informix  25M Dec 20 09:21 P12800.7*
2.4M -rwxrwxrwx 1 sdc informix 2.4M Dec 19 13:40 P31744.7*
2.4M -rwxrwxrwx 1 sdc informix 2.4M Dec 19 13:29 P30208.7*
 26M -rwxrwxrwx 1 sdc informix  26M Dec 19 13:28 P29696.7*
2.4M -rwxrwxrwx 1 sdc informix 2.4M Dec 19 13:25 P28672.7*
2.4M -rwxrwxrwx 1 sdc informix 2.4M Dec 19 13:12 P26624.7*
 25M -rwxrwxrwx 1 sdc informix  25M Dec 17 08:28 P05632.7*
 26M -rwxrwxrwx 1 sdc informix  26M Dec 13 14:49 P73216.7*
 65M -rwxrwxrwx 1 sdc informix  65M Dec 13 14:43 P72192.7*
2.4M -rwxrwxrwx 1 sdc informix 2.4M Dec 13 14:37 P71168.7*
 65M -rwxrwxrwx 1 sdc informix  65M Dec 13 14:36 P70656.7*
2.4M -rwxrwxrwx 1 sdc informix 2.4M Dec 13 14:31 P69632.7*
2.4M -rwxrwxrwx 1 sdc informix 2.4M Dec 13 14:23 P68096.7*
2.4M -rwxrwxrwx 1 sdc informix 2.4M Dec 13 14:20 P67072.7*
2.4M -rwxrwxrwx 1 sdc informix 2.4M Dec 13 14:13 P66048.7*
2.4M -rwxrwxrwx 1 sdc informix 2.4M Dec 13 14:12 P65024.7*
380K -rwxrwxrwx 1 sdc informix 378K Dec 13 11:02 P58368.7*
636K -rwxrwxrwx 1 sdc informix 634K Dec 13 10:56 P56832.7*
"""

# Check names one by one for matching MRN.

# Retrieve all subjects with the MRN.

# Close connection.

# Log incident.