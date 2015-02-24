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

# https://dev.mysql.com/doc/connector-python/en/connector-python-example-ddl.html


from __future__ import print_function

import mysql.connector
from mysql.connector import errorcode
import config# Settings




DB_NAME = config.sql_login["database"]

TABLES = {}
# The metadata associated with a story, as given by the API page for a story
TABLES['story_metadata'] = (
    "CREATE TABLE `story_metadata` ("
    # Local stuff
    "  `primary_key` int NOT NULL AUTO_INCREMENT,"# Is used only as primary key
    "  `version` int NOT NULL,"# The version of this story this row is associated with
    # From site
    "  `status` text NOT NULL,"
    "  `total_views` int NOT NULL,"
    "  `full_image` text,"
    "  `description` text NOT NULL,"
    "  `views` int NOT NULL,"
    "  `date_modified` int NOT NULL,"
    "  `url` text NOT NULL,"
    "  `image` text,"
    "  `title` text NOT NULL,"
    "  `dislikes` int NOT NULL,"
    "  `comments` int NOT NULL,"
    "  `content_rating` int NOT NULL,"
    "  `chapter_count` int NOT NULL,"
    # chapters [??]
    # author {name (string),id (int)}
    "  `author_name` varchar(64) NOT NULL,"# [19:17] <&twkr> author_name is varchar(64) on fimfiction.
    "  `author_id` int NOT NULL,"
    "  `words` int NOT NULL,"
    "  `content_rating_text` text NOT NULL,"
    "  `short_description` text NOT NULL,"
    "  `id` int NOT NULL,"# id is name used in API, referred to as story_id elsewhere to avoid confusion
    # categories {??}
    "  `likes` int NOT NULL,"
    "  PRIMARY KEY (`primary_key`)"
    ") ENGINE=InnoDB")

# The metadata associated with a chapter, as given by the API page for a story
TABLES['chapter_metadata'] = (
    "CREATE TABLE `chapter_metadata` ("
    # Local stuff
    "  `primary_key` int NOT NULL AUTO_INCREMENT,"# Is used only as primary key
    "  `version` int NOT NULL,"# The version of this story this row is associated with
    "  `parent_story_id` int NOT NULL,"# The site-assigned ID for a story
    "  `chapter_number` int NOT NULL,"# Determined based on order chapters appear in API
    # From site
    "  `id` int NOT NULL,"# id is name used in API, referred to as story_id elsewhere to avoid confusion
    "  `link` text,"
    "  `title` text NOT NULL,"
    "  `views` int NOT NULL,"
    "  `words` int NOT NULL,"
    "  PRIMARY KEY (`primary_key`)"
    ") ENGINE=InnoDB")

# The text for an individual chapter, as given bu the chapter download links
TABLES['chapter_texts'] = (
    "CREATE TABLE `chapter_texts` ("
    # Local stuff
    "  `primary_key` int NOT NULL AUTO_INCREMENT,"# Is used only as primary key
    "  `version` int NOT NULL,"# The version of this story this row is associated with
    "  `parent_chapter_id` int NOT NULL,"
    "  `parent_story_id` int NOT NULL,"
    "  `chapter_number` int NOT NULL,"
    # From site
    "  `chapter_text`  MEDIUMTEXT NOT NULL,"# Was told by twkr that the site used MEDIUMTEXT for chapters
    "  `chapter_html`  MEDIUMTEXT NOT NULL,"# Was told by twkr that the site used MEDIUMTEXT for chapters
    "  PRIMARY KEY (`primary_key`)"
    ") ENGINE=InnoDB")

# The full text of a story, as given by the full story download links
TABLES['full_texts'] = (
    "CREATE TABLE `full_texts` ("
    # Local stuff
    "  `primary_key` int NOT NULL AUTO_INCREMENT,"# Is used only as primary key
    "  `version` int NOT NULL,"# The version of this story this row is associated with
    "  `parent_story_id` int NOT NULL,"# The site-assigned ID for a story
    # From site
    "  `full_story_text` LONGTEXT,"# Was told by twkr that the site used MEDIUMTEXT for chapters, so use next size up
    "  `full_story_html` LONGTEXT,"# Was told by twkr that the site used MEDIUMTEXT for chapters, so use next size up
    "  PRIMARY KEY (`primary_key`)"
    ") ENGINE=InnoDB")

# Category information for each story, as given by the API
TABLES['story_categories'] = (
    "CREATE TABLE `story_categories` ("
    # Local stuff
    "  `primary_key` int NOT NULL AUTO_INCREMENT,"# Is used only as primary key
    "  `version` int NOT NULL,"# The version of this story this row is associated with
    "  `parent_story_id` int NOT NULL,"# The site-assigned ID for a story
    # From site
    "  `Dark` bool,"
    "  `Slice of Life` bool,"
    "  `Anthro` bool,"
    "  `Random` bool,"
    "  `Alternate Universe` bool,"
    "  `Sad` bool,"
    "  `Romance` bool,"
    "  `Crossover` bool,"
    "  `Adventure` bool,"
    "  `Human` bool,"
    "  `Comedy` bool,"
    "  `Tragedy` bool,"
    "  PRIMARY KEY (`primary_key`)"
    ") ENGINE=InnoDB")




def setup_max_size(connection):
    cursor =  connection.cursor()
    query = (
    "set global net_buffer_length=1000000;"
    "set global max_allowed_packet=1000000000;"
    )
    result = cursor.execute(query)
    return





def create_database(cursor):
    try:
        cursor.execute(
            "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(DB_NAME))
    except mysql.connector.Error as err:
        print("Failed creating database: {}".format(err))
        exit(1)













def main():
    cnx = mysql.connector.connect(**config.sql_login)
    cursor = cnx.cursor()
    try:
        cnx.database = DB_NAME
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)



    for name, ddl in TABLES.iteritems():
        try:
            print("Creating table {}: ".format(name), end='')
            cursor.execute(ddl)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            print(err.msg)
        else:
            print("OK")

    cursor.close()
    setup_max_size(cnx)
    cnx.close()


if __name__ == '__main__':
    main()
