import csv
import os
import sys

''' CONFIG '''

# PATHS
''' Path relative to this script for input data files '''
input_path = './data'

''' Path relative to this script for output data files '''
output_path = './output'


# OpenBCI SETTINGS

'''
OBCI data doesn't include a timestamp. We'll calculate the
timestamps based on the sample rate.
'''

input_sample_rate = 125

''' END CONFIG '''

input_headers = ['id','chan1','chan2','chan3','chan4','chan5','chan6','chan7','chan8','accel1','accel2','accel3'];
output_headers = ['Time','chan1','chan2','chan3','chan4','chan5','chan6','chan7','chan8','Sample_rate']

files = os.listdir(input_path)

csv_files = [

"OpenBCI-RAW-2019-09-25_04-55-39.txt",
 "OpenBCI-RAW-2019-09-25_04-59-08.txt",
 "OpenBCI-RAW-2019-09-25_05-25-36.txt",
 "OpenBCI-RAW-2019-09-25_05-27-19.txt",
 "OpenBCI-RAW-2019-09-25_05-38-49.txt",
 "OpenBCI-RAW-2019-09-25_05-43-07.txt",
 "OpenBCI-RAW-2019-09-26_03-28-21.txt",
 "OpenBCI-RAW-2019-09-26_03-30-42.txt",
 "OpenBCI-RAW-2019-09-26_04-37-15.txt",
 "OpenBCI-RAW-2019-09-26_04-39-28.txt",
"OpenBCI-RAW-2019-10-05_15-07-34 rest.txt",
"OpenBCI-RAW-2019-10-05_15-10-57 harvard step test.txt",
 "OpenBCI-RAW-2020-05-13_11-59-14.txt",

]
for filename in files:
  if '.txt' in filename:
    csv_files.append(filename)
    
print(csv_files)

if(len(csv_files) < 1):
  print "ERROR: No input files found! \n Input files must be placed in the '"+input_path+"' directory  (relative \n to  the location of this script), or change the 'input_path'\n parameter in the script"
  raw_input()
  
for input_fn in csv_files:

  print "Processing file: "+input_fn+" ... "

  output_data = []

  time_counter = 0
  time_increment = float(1)/float(input_sample_rate)

  print "Sample rate: "+str(input_sample_rate)+" ... "
  print "Time increment: "+str(time_increment)+" ... "


  with open(os.path.join(input_path,input_fn), 'rb') as csvfile:


     for i, line in enumerate(csvfile):
          if i == 2:
            sr_line = line
            break

     input_sample_rate = sr_line[15:21]

     csv_input = csv.DictReader(csvfile, fieldnames=input_headers, dialect='excel')
     row_count = 0

     for row in csv_input:

          row_count = row_count + 1

          if(row_count > 2):

            output = {}

            time_counter = time_counter + time_increment

            output['Time'] = time_counter

            for i in range(1,9):
              channel_key = 'chan'+str(i)
              output[channel_key] = row[channel_key]

            output['Sample_rate'] = input_sample_rate

            output_data.append(output)



  output_fn = "converted_"+input_fn

  output_csv_file = open(os.path.join(output_path,output_fn), 'wb')

  csv_output = csv.DictWriter(output_csv_file, fieldnames=output_headers, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

  headers_text = {}

  for val in output_headers:
    headers_text[val] = val

  csv_output.writerow(headers_text)

  for row in output_data:
    csv_output.writerow(row)

  output_csv_file.close()
