#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     15/02/2015
# Copyright:   (c) User 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------





# File paths
root_path = "download"

# SQL Stuff
sql_login = {
  'user': 'root',# Username for DB connection
  'password': 'toor',# Password for DB
  'host': '127.0.0.1',# Host IP for DB
  'database': 'fimfic',# Database name for DB
  'raise_on_warnings': True,
}


# Run parameters
# Check range
process_range = True# Should we run over a specified range? (BOOLEAN)
start_id = 1# ID of range start (INT)
finish_id = 300000# ID of range end (INT)




def main():
    pass

if __name__ == '__main__':
    main()
