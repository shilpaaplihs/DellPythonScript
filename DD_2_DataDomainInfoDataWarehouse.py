#!/usr/bin/env python
# coding: utf-8

# # Data Domain Information – DataWarehouse

# In[5]:


#Packages required for the project
import requests
import time
import urllib.request
import xml.etree.ElementTree as ET
from urllib.request import urlopen
import warnings
warnings.filterwarnings('ignore')
import datetime
timetime = time.strftime("%Y%m%d-%H%M%S")
#print (timetime)
import os
import csv


# In[6]:


#Function to save the file
def saveFile(data):
    with open('C:/PYTHON DOWNLOAD/DD2_Info_' + timetime + '.csv','w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames = ['Hostname', 'Filesystem', 'Capacity(GB)', 'UsedSpace(GB)', 'Utilization(%)', 'AvailableCapacity(GB)', 'CleanableSpace(GB)', 'Model', 'CleanStatus', 'CleanSchedule', 'CleanThrottle', 'OSVersion', 'Noted'])
        writer.writeheader()
        for line in data: 
            for dd in line:
                f.write(dd)
                f.write("\n")


# In[7]:


#'100.64.12.131' -USDC2 some issue 
#Details required for report generation
xval_DC= ['100.96.67.11:9002', '100.96.3.11:9002','100.64.227.12:9002', '100.65.147.12:9002','100.64.51.12:9002', '100.64.99.12:9002',
'100.64.35.12:9002','100.64.147.12:9002','192.168.61.86:9002', '10.48.6.19:9002','10.48.70.19:9002','100.97.3.11:9002','100.96.131.11:9002','100.96.195.11:9002','100.98.3.11:9002']
url_part1 = 'https://'
url_part2 = '/dpa-api/report'
payload = "<runReportParameters>\r\n<report>\r\n<name>Data Domain Information - DataWarehouse</name> <!-- Report template name -->     </report>\r\n<nodes>         \r\n<node>\r\n<id>2dbd754e-8e3f-4397-b4cd-d9f11a913fe9</id> <!-- scope -  node id of the Host -->\r\n</node>     \r\n</nodes>\r\n<timeConstraints type=\"window\">       \r\n<window >           \r\n<name>Last Day</name> <!-- time period name -->         \r\n</window>     \r\n</timeConstraints>    \r\n<formatParameters>        \r\n<formatType>CSV</formatType> <!-- format type, could be CSV, HTML, PDF, IMAGE, XML. -->     </formatParameters></runReportParameters>"
headers = {
    'Content-Type': "application/vnd.emc.apollo-v1+xml",
    'Authorization': "Basic Ym9vbWkuaW50ZWdyYXRpb246Qm9vbWlAMTIz",
    }


# In[8]:


#Downloading data from server and saving in local
succeeded_req = []
failed_req = []

for x in xval_DC[0:]:
    full_url = url_part1 + x + url_part2
    response = requests.request("POST", full_url, data=payload, headers=headers, verify=False)
    print (response.status_code)
    if response.status_code < 399:
        link = ET.fromstring(response.text)
        reportLink = link.find("link").text
        counter = 0
        max_attempt_allowed = 5
        while (counter <= max_attempt_allowed):
            r = requests.get(reportLink, headers=headers, verify=False)
            #print ("code for {} at attempt {}: {}".format(x, counter+1, r.status_code))
            if r.status_code > 399:
                counter += 1
                time.sleep(5)
            else:
                data = r.text
                data = data.split("\n")
                succeeded_req.append(data[1:])
                break
                
saveFile(succeeded_req)
print('The report has been downloaded successfully.')


# In[9]:


# error handling code
        #if(counter >= max_attempt_allowed):
            #print("ERROR: {} after {} attemps".format(x, max_attempt_allowed))
            #failed_req.append(x)
#print("{} succeded out of {}".format(len(succeeded_req), len(xval_DC)))     
#print("{} Failed out of {}".format(len(failed_req), len(xval_DC))) 


# In[ ]:




