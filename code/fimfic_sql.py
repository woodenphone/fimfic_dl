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
import json
import mysql.connector
from utils import *



def find_highest_story_version(story_id):
    find_versions_query = ""
    return version_number

def insert_json(story_json):
    story_api_dict = json.loads(story_json)
    values ={
    "author_id":"",
    "author_name":"",
    "categories":"",
    "chapters":"",
    "comments":"",
    "content_rating":"",
    "content_rating_text":"",
    "date_modified":"",
    "description":"",
    "dislikes":"",
    "full_image":"",
    "story_id":"",
    "image":"",
    "likes":"",
    "short_description":"",
    "status":"",
    "title":"",
    "total_vievs":"",
    "url":"",
    "views":"",
    "words":"",
    "version_number":"",
    "folder_path":"",
    }

    fields = values.keys()
    values = values.values()

    cursor.execute(
    "INSERT INTO table (%s) VALUES (%%s);" % (",".join(fields)),
    *values
    )






def insert_story_metadata(api_dict,version=1):
    logging.debug("Inserting into story_metadata")
    story_dict = api_dict["story"]
    # Table: story_metadata

    story_metadata_values = {
    "version":version,
    "status":story_dict["status"],#1
    "total_views":story_dict["total_views"],
    "full_image":story_dict["full_image"],
    "description":story_dict["description"],
    "views":story_dict["views"],#5
    "date_modified":story_dict["date_modified"],
    "url":story_dict["url"],
    "image":story_dict["image"],
    "title":story_dict["title"],
    "dislikes":story_dict["dislikes"],# 10
    "comments":story_dict["comments"],
    "content_rating":story_dict["content_rating"],
    "chapter_count":story_dict["chapter_count"],
    "author_name":story_dict["author"]["name"],
    "author_id":story_dict["author"]["id"],# 15
    "words":story_dict["words"],
    "content_rating_text":story_dict["content_rating_text"],
    "short_description":story_dict["short_description"],
    "id":story_dict["id"],
    "likes":story_dict["likes"],# 20
    }

    fields = story_metadata_values.keys()
    values = story_metadata_values.values()
#    query = "INSERT INTO story_metadata (%s) VALUES (%%s);" % (",".join(fields))
    query = ("INSERT INTO story_metadata (%s)"" VALUES ("
    "%%s, "# 1
    "%%s, "
    "%%s, "
    "%%s, "
    "%%s, "# 5
    "%%s, "
    "%%s, "
    "%%s, "
    "%%s, "
    "%%s, "# 10
    "%%s, "# 11
    "%%s, "
    "%%s, "
    "%%s, "
    "%%s, "# 15
    "%%s, "
    "%%s, "
    "%%s, "
    "%%s, "
    "%%s, "# 20
    "%%s"# 21
    ");"
    % (",".join(fields))
    )
    print repr(query)
    cursor.execute(query, values)
    cnx.commit()
    return


def insert_chapter_metadata(api_dict,parent_story_id,version=1):
    logging.debug("Inserting into chapter_metadata")
    story_dict = api_dict["story"]
    chapters_list = story_dict["chapters"]
    # Table: chapter_metadata
    chapter_number_counter = 0
    for chapter_dict in chapters_list:
        chapter_number_counter += 1

        chapter_metadata_values = {
        # Local stuff
        "version":version,
        "parent_story_id":parent_story_id,
        "chapter_number":chapter_number_counter,
        # From API
        "id":story_dict["id"],
        "link":story_dict["link"],
        "title":story_dict["title"],
        "views":story_dict["views"],
        "words":story_dict["words"],
        }

        fields = chapter_metadata_values.keys()
        values = chapter_metadata_values.values()
        cursor.execute(
        "INSERT INTO table (%s) VALUES (%%s);" % (",".join(fields),),
        *values
        )
    return



def find_story_id(api_dict):
    return api_dict["story"]["id"]


def find_newest_version(story_id):
    logging.debug("Finding latest version number for"+repr(story_id))
    # Find highest in each table
    tables_and_id_fields = {
    "story_metadata":"id",
    "chapter_metadata":"parent_story_id",
    "chapter_texts":"parent_story_id",
    "full_texts":"parent_story_id",
    "story_categories":"parent_story_id",
    }
    for table_name in tables_and_id_fields:
        query = (
        "SELECT * FROM story_metadata WHERE id = %s ORDER BY version LIMIT 1"
        )
        cursor.execute(query, (story_id))
    # Return highest seen
    return 0# latest_version_number






def show_api_structure():
    with open("api.json", "rb") as file:
        story_json = file.read()
    initial_story_api_dict = json.loads(story_json)
    story_api_dict = initial_story_api_dict["story"]
    #insert_json(story_json)
    for key in story_api_dict.keys():
        print repr(key)+""+repr(type(story_api_dict[key]))


def main():
    setup_logging(log_file_path=os.path.join("debug","fimfic-dl-sql-log.txt"))
    pass

if __name__ == '__main__':
    main()




cnx = mysql.connector.connect(**config.sql_login)
cursor = cnx.cursor()



with open("api.json", "rb") as file:
    story_json = file.read()
    story_api_dict = json.loads(story_json)
insert_story_metadata(story_api_dict)


cnx.close()
