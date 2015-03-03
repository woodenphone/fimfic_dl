#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      User
#
# Created:     01/02/2015
# Copyright:   (c) User 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------


import config
#import json
import mysql.connector
from utils import *


def generate_insert_query(table_name,value_names):
    """Generate a SQL insert statement so all the statements can be made in one place
    NEVER LET THIS TOUCH OUTSIDE DATA!
    'INSERT INTO <TABLE_NAME> (<VALUE_NAME_1>, <VALUE_NAME_2>,...) %s, %s, ...);'
    """
    assert len(value_names) > 0
    value_names_with_backticks = []
    for value in value_names:
        assert(type(value) is type(""))
        value_names_with_backticks.append("`"+value+"`")
    query = (
    "INSERT INTO `"+table_name+"` (%s) VALUES (" % (", ".join(value_names_with_backticks),)# Values from dict
    +"%s, "*(len(value_names_with_backticks)-1)#values to insert
    +"%s);"
    )
    #logging.debug(repr(query))
    return query


def insert_json(connection,story_json):
    """Used for testing during development?"""
    cursor =  connection.cursor()
    story_api_dict = json.loads(story_json)
    values = {
    "author_id":"",#1
    "author_name":"",
    "categories":"",
    "chapters":"",
    "comments":"",#5
    "content_rating":"",
    "content_rating_text":"",
    "date_modified":"",
    "description":"",
    "dislikes":"",#10
    "full_image":"",
    "story_id":"",
    "image":"",
    "likes":"",
    "short_description":"",
    "status":"",
    "title":"",
    "total_vievs":"",
    "url":"",
    "views":"",#20
    "words":"",
    "version_number":"",
    "folder_path":"",#23
    }
    fields=values.keys()
    values = values.values()
    query = generate_insert_query(table_name="chapter_metadata",value_names=fields)
    logging.debug(repr(query))
    result = cursor.execute(query,values)
    cursor.close()
    return


def insert_story_metadata(connection,api_dict,version):
    assert(type(version) is type(1)) # Check input
    cursor = connection.cursor()
    logging.debug("Inserting into story_metadata")
    story_dict = api_dict["story"]
    # Table: story_metadata
    story_metadata_values = {
    # Local values
    "version":version,
    "date_saved":get_current_unix_time(),
    # Remote values from API
    "status":story_dict["status"],
    "total_views":story_dict["total_views"],
    "full_image":(story_dict["full_image"] if ("full_image" in story_dict.keys()) else None),
    "description":story_dict["description"],
    "views":story_dict["views"],
    "date_modified":story_dict["date_modified"],
    "url":story_dict["url"],
    "image":(story_dict["image"] if ("image" in story_dict.keys()) else None),
    "title":story_dict["title"],
    "dislikes":story_dict["dislikes"],
    "comments":story_dict["comments"],
    "content_rating":story_dict["content_rating"],
    "chapter_count":story_dict["chapter_count"],
    "author_name":story_dict["author"]["name"],
    "author_id":story_dict["author"]["id"],
    "words":story_dict["words"],
    "content_rating_text":story_dict["content_rating_text"],
    "short_description":story_dict["short_description"],
    "id":story_dict["id"],
    "likes":story_dict["likes"],
    }
    fields = story_metadata_values.keys()
    values = story_metadata_values.values()
    query = generate_insert_query(table_name="story_metadata",value_names=fields)
    logging.debug(repr(query))
    result = cursor.execute(query, values)
    cursor.close()
    return


def insert_category_metadata(connection,api_dict,parent_story_id,version):
    """Insert category data into the DB"""
    cursor =  connection.cursor()
    row_to_insert = {
    # Local
    "version":version,
    "parent_story_id":parent_story_id,
    # Site
    "Dark":api_dict["story"]["categories"]["Dark"],
    "Slice of Life":api_dict["story"]["categories"]["Slice of Life"],
    "Anthro":api_dict["story"]["categories"]["Anthro"],
    "Random":api_dict["story"]["categories"]["Random"],
    "Alternate Universe":api_dict["story"]["categories"]["Alternate Universe"],
    "Sad":api_dict["story"]["categories"]["Sad"],
    "Romance":api_dict["story"]["categories"]["Romance"],
    "Crossover":api_dict["story"]["categories"]["Crossover"],
    "Adventure":api_dict["story"]["categories"]["Adventure"],
    "Human":api_dict["story"]["categories"]["Human"],
    "Comedy":api_dict["story"]["categories"]["Comedy"],
    "Tragedy":api_dict["story"]["categories"]["Tragedy"],
    }
    fields = row_to_insert.keys()
    values = row_to_insert.values()
    query = generate_insert_query(table_name="story_categories",value_names=fields)
    logging.debug(repr(query))
    result = cursor.execute(query, values)
    cursor.close()
    return


def insert_chapter_metadata(connection,api_dict,parent_story_id,version):
    """Insert the metadata for a chapter into the DB"""
    assert(type(version) is type(1)) # Check input
    assert(type(parent_story_id) is type(1))
    cursor =  connection.cursor()
    logging.debug("Inserting into chapter_metadata")
    story_dict = api_dict["story"]
    chapters_list = story_dict["chapters"]
    # Table: chapter_metadata
    chapter_number_counter = 0
    for chapter_dict in chapters_list:
        chapter_number_counter += 1
        chapter_metadata_values = {
        # Local stuff
        "version":version,#1
        "parent_story_id":parent_story_id,
        "chapter_number":chapter_number_counter,
        # From API
        "id":story_dict["id"],
        # Ternary shit because API sometimes omits fields
        "link":(story_dict["link"] if ("link" in story_dict.keys()) else None),
        "title":(story_dict["title"] if ("title" in story_dict.keys()) else None),
        "views":(story_dict["views"] if ("views" in story_dict.keys()) else None),
        "words":(story_dict["words"] if ("words" in story_dict.keys()) else None),#8
        }
        fields = chapter_metadata_values.keys()
        values = chapter_metadata_values.values()
        query = generate_insert_query(table_name="chapter_metadata",value_names=fields)
        logging.debug(repr(query))
        result = cursor.execute(query,values)
        continue
    cursor.close()
    return


def insert_chapter_text(connection,parent_story_id,chapter_id,chapter_number,version,html=None,txt=None,epub=None):
    """Insert the text of a chapter into the DB"""
    assert(type(parent_story_id) is type(1)) # Check input
    assert(type(chapter_id) is type(1))
    assert(type(chapter_number) is type(1))
    assert(type(version) is type(1))
    cursor =  connection.cursor()
    chapter_to_insert = {
    "version":version,#1
    "parent_chapter_id":chapter_id,
    "parent_story_id":parent_story_id,
    "chapter_number":chapter_number,
    "chapter_text":txt,#5
    "chapter_html":html,#6
    }
    fields = chapter_to_insert.keys()
    values = chapter_to_insert.values()
    query = generate_insert_query(table_name="chapter_texts",value_names=fields)
    logging.debug(repr(query))
    result = cursor.execute(query,values)
    cursor.close()
    return


def insert_full_text(connection,parent_story_id,version,full_story_text=None,full_story_html=None):
    """Insert the full text for a story into the DB"""
    assert(type(parent_story_id) is type(1)) # Check input
    cursor =  connection.cursor()
    row_to_insert = {
    "parent_story_id":parent_story_id,
    "version":version,
    "full_story_text":full_story_text,
    "full_story_html":full_story_html,
    }
    fields = row_to_insert.keys()
    values = row_to_insert.values()
    query = generate_insert_query(table_name="full_texts",value_names=fields)
    result = cursor.execute(query,values)
    cursor.close()
    return


def find_newest_version(connection,story_id):
    """Find the highest version number associated with a story_id"""
    assert(type(story_id) is type(1)) # Check input
    cursor =  connection.cursor()
    logging.debug("Finding latest version number for"+repr(story_id))
    query = (
    "SELECT version FROM (story_metadata) WHERE id = %s ORDER BY version LIMIT 1"
    )
    logging.debug(repr(query))
    cursor.execute(query, (int(story_id),))
    row_counter = 0
    for row in cursor:
        row_counter += 1
        version = row[0]
    if row_counter == 0:
        version = None
    logging.debug("Latest version found: "+repr(version))
    cursor.close()
    return version



def lookup_date(connection,story_id,version):
    """Look up and return the unix time date stamp of version of a story
    return None if no version found"""
    assert(type(story_id) is type(1)) # Check input
    assert(type(version) is type(1))
    cursor =  connection.cursor()
    query = ("SELECT date_modified FROM story_metadata "
         "WHERE id = %s AND version = %s")
    logging.debug(repr(query))
    result = cursor.execute(query, (story_id, version))
    row_counter = 0
    for row in cursor:
        row_counter += 1
        date_modified = row[0]
        print repr(row)
    if row_counter == 0:
        logging.debug("No date associated with ID/Version combination")
        date_modified = None
    cursor.close()
    return date_modified


def show_api_structure():
    with open("api.json", "rb") as file:
        story_json = file.read()
    initial_story_api_dict = json.loads(story_json)
    story_api_dict = initial_story_api_dict["story"]
    #insert_json(story_json)
    for key in story_api_dict.keys():
        print repr(key)+""+repr(type(story_api_dict[key]))


def main():
    return # Code not needed outside debugging
    setup_logging(log_file_path=os.path.join("debug","fimfic-dl-sql-log.txt"))

    cnx = mysql.connector.connect(**config.sql_login)
    cursor = cnx.cursor()
    cursor.close()

    with open("api.json", "rb") as file:
        story_json = file.read()
        story_api_dict = json.loads(story_json)
    insert_story_metadata(cnx,story_api_dict,version=1)

    cnx.close()

if __name__ == '__main__':
    main()

