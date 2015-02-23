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
TABLES['story_metadata'] = (
    "CREATE TABLE `story_metadata` ("
    # Local stuff
    "  `primary_key` int NOT NULL AUTO_INCREMENT,"
    "  `version` int NOT NULL,"
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
    "  `author_name` text NOT NULL,"
    "  `author_id` int NOT NULL,"
    "  `words` int NOT NULL,"
    "  `content_rating_text` text NOT NULL,"
    "  `short_description` text NOT NULL,"
    "  `id` int NOT NULL,"
    # categories {??}
    "  `likes` int NOT NULL,"
    "  PRIMARY KEY (`primary_key`)"
    ") ENGINE=InnoDB")


TABLES['chapter_metadata'] = (
    "CREATE TABLE `chapter_metadata` ("
    # Local stuff
    "  `primary_key` int NOT NULL AUTO_INCREMENT,"
    "  `version` int NOT NULL,"
    "  `parent_story_id` int NOT NULL,"
    "  `chapter_number` int NOT NULL,"
    # From site
    "  `id` int NOT NULL,"
    "  `link` text,"
    "  `title` text NOT NULL,"
    "  `views` int NOT NULL,"
    "  `words` int NOT NULL,"
    "  PRIMARY KEY (`primary_key`)"
    ") ENGINE=InnoDB")


TABLES['chapter_texts'] = (
    "CREATE TABLE `chapter_texts` ("
    # Local stuff
    "  `primary_key` int NOT NULL AUTO_INCREMENT,"
    "  `version` int NOT NULL,"
    "  `parent_chapter_id` int NOT NULL,"
    "  `parent_story_id` int NOT NULL,"
    "  `chapter_number` int NOT NULL,"
    # From site
    "  `chapter_text`  MEDIUMTEXT NOT NULL,"
    "  `chapter_html`  MEDIUMTEXT NOT NULL,"
    "  PRIMARY KEY (`primary_key`)"
    ") ENGINE=InnoDB")


TABLES['full_texts'] = (
    "CREATE TABLE `full_texts` ("
    # Local stuff
    "  `primary_key` int NOT NULL AUTO_INCREMENT,"
    "  `version` int NOT NULL,"
    "  `parent_story_id` int NOT NULL,"
    # From site
    "  `full_story_text` LONGTEXT,"
    "  `full_story_html` LONGTEXT,"
    "  PRIMARY KEY (`primary_key`)"
    ") ENGINE=InnoDB")


TABLES['story_categories'] = (
    "CREATE TABLE `story_categories` ("
    # Local stuff
    "  `primary_key` int NOT NULL AUTO_INCREMENT,"
    "  `version` int NOT NULL,"
    "  `parent_story_id` int NOT NULL,"
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
