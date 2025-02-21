#!/usr/bin/env python
import sys
from module_utils.sap_id_sso import sap_sso_login
from module_utils.sap_launchpad_software_center_download_runner import *

input_search_file_list=sys.argv[1]
username = sys.argv[2]
password = sys.argv[3]

sap_sso_login(username, password)

input_search_file_list_python=iter(input_search_file_list.splitlines())

for item in input_search_file_list_python:
  try:
    download_link, download_filename = search_software_filename(item,'')
  except Exception as e:
    print(item)
    continue
