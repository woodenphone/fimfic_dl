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





from utils import *
from fimfic_sql import *


def generate_story_filename(date_modified,story_id,version,chapter_number=None,ext="htm"):
    """Generate a filename for a story file
    unixtime.id.version.(full|chapter.n).ext
    determines if chapter or full by chapter_number variable"""
    if chapter_number:
        filename = str(date_modified)+"."+str(story_id)+"."+str(version)+".chapter."+str(chapter_number)+"."+ext
    else:
        filename = str(date_modified)+"."+str(story_id)+"."+str(version)+".full."+ext
    return filename


def generate_full_path(root_path,story_id,version_number,filename):
    """Generate storage filepath
    ###/###/###/V#/filename
    Millions / Thousands / Ones / V Version_number / filename
    root_path/000/000/001/V1/filename.ext
    root_path/999/999/999/V99999/filename.ext"""
    assert(type(story_id) is int)# Must be integer
    assert(type(version_number) is int)# Must be integer
    assert(0 <= story_id <= 999999999)# Between zero and 999,999,999
    assert(1 <= version_number <= 999999999)# Between zero and 999,999,999

    padded_story_id_string = str(story_id).zfill(9)

    millions_section = padded_story_id_string[0:3]
    thousands_section = padded_story_id_string[3:6]
    ones_section = padded_story_id_string[6:9]

    version_section = "v"+str(version_number)

    file_path = os.path.join(
    root_path,
    millions_section,
    thousands_section,
    ones_section,
    version_section,
    filename
    )
    return file_path


def generate_story_folder_path(root_path,story_id):
    """Generate storage filepath
    ###/###/###/V#/filename
    Millions / Thousands / Ones / V Version_number / filename
    root_path/000/000/001/
    root_path/999/999/999/"""
    assert(type(story_id) is int)# Must be integer
    assert(0 <= story_id <= 999999999)# Between zero and 999,999,999

    padded_story_id_string = str(story_id).zfill(9)

    millions_section = padded_story_id_string[0:3]
    thousands_section = padded_story_id_string[3:6]
    ones_section = padded_story_id_string[6:9]

    file_path = os.path.join(
    root_path,
    millions_section,
    thousands_section,
    ones_section
    )
    return file_path


def check_if_story_exists(api_dict):
    """Given a decoded API json, see if it looks like the story exists"""
    if "error" in api_dict.keys():
        if api_dict["error"] == "Invalid story id":
            logging.debug("Story ID not valid.")
            return False
    elif "story" in api_dict.keys():
        return True
    else:
        logging.error("Unexpected API data contents!")
        logging.error(repr(locals()))
        raise ValueError


def save_story_images(connection,root_path,story_id,api_dict,version):
    """Try to save any images associated with a story in the API to the story's base folder
    Only one version of a story's image will be saved to save bandwidth and disk space.
    example output path: "download/000/000/001/full_image.jpg"
    """
    story_path = generate_story_folder_path(root_path,story_id)
    # Try saving "full_image" field
    if "full_image" in api_dict["story"].keys:
        full_image_url = api_dict["story"]["full_image"]
        full_image = get(full_image_url)
        full_image_filename = os.path.split(full_image_url)[1]
        full_image_path = os.path.join(story_path, full_image_filename)
        save_file(full_image_path,full_image)
    # Try saving "image" field
    if "image" in api_dict["story"].keys:
        image_url = api_dict["story"]["image"]
        image = get(image_url)
        image_filename = os.path.split(image_url)[1]
        image_path = os.path.join(story_path, image_filename)
        save_file(image_path,image)
    return



def save_story(connection,root_path,story_id,api_dict,raw_api_json,version):
    """Download a story and add it to the DB"""
    logging.info("Downloading story "+repr(story_id))
    date_modified = api_dict["story"]["date_modified"]
    # Download full story and save to file
    # HTML
    full_story_html_url = "http://www.fimfiction.net/download_story.php?story="+str(story_id)+"&html"
    full_story_html = get(full_story_html_url)
    full_story_html_filename = generate_story_filename(date_modified,story_id,version,chapter_number=None,ext="htm")
    full_story_html_path = generate_full_path(root_path,story_id,version,full_story_html_filename)
    save_file(full_story_html_path,full_story_html)
    # TXT
    full_story_txt_url = "http://www.fimfiction.net/download_story.php?story="+str(story_id)
    full_story_txt = get(full_story_txt_url)
    full_story_txt_filename = generate_story_filename(date_modified,story_id,version,chapter_number=None,ext="txt")
    full_story_txt_path = generate_full_path(root_path,story_id,version,full_story_txt_filename)
    save_file(full_story_txt_path,full_story_txt)
    # EPUB
    full_story_epub_url = "http://www.fimfiction.net/download_epub.php?story="+str(story_id)
    # Add full story to DB
    insert_full_text(connection,story_id,version,full_story_text=None,full_story_html=full_story_html)
    # Download chapters
    number_of_chapters = api_dict["story"]["chapter_count"]
    if number_of_chapters == 0:
        logging.error("Zero chapters for this story!")
    else:
        chapters = api_dict["story"]["chapters"]
        chapter_number = 0
        for chapter in chapters:
            chapter_number += 1
            chapter_id = chapter["id"]
            chapter_html_url = "http://www.fimfiction.net/download_chapter.php?chapter="+str(chapter_id)+"&html"
            chapter_txt_url = "http://www.fimfiction.net/download_chapter.php?chapter="+str(chapter_id)
            # Load chapter from server and save to disk
            # HTML
            chapter_html = get(chapter_html_url)
            chapter_html_filename = generate_story_filename(date_modified,story_id,version,chapter_number,ext="htm")
            chapter_html_path = generate_full_path(root_path,story_id,version,chapter_html_filename)
            save_file(chapter_html_path,chapter_html)
            # TXT
            chapter_txt = get(chapter_txt_url)
            chapter_txt_filename = generate_story_filename(date_modified,story_id,version,chapter_number,ext="txt")
            chapter_txt_path = generate_full_path(root_path,story_id,version,chapter_txt_filename)
            save_file(chapter_txt_path,chapter_txt)
            # Add chapter to DB
            insert_chapter_text(connection,story_id,chapter_id,chapter_number,version,html=chapter_html,txt=chapter_txt,epub=None)
            continue
        # Insert chapter metadata entries
        insert_chapter_metadata(connection,api_dict,story_id,version)
    # Save API metadata JSON to file
    json_filename = str(story_id)+".v"+str(version)+".json"
    json_path = generate_full_path(root_path,story_id,version,json_filename)
    # Add API metadata to DB
    insert_story_metadata(connection,api_dict,version=1)
    # Add category metadata to DB
    insert_category_metadata(connection,api_dict,story_id,version)
    # Commit/save new data
    connection.commit()
    logging.info("Saved "+repr(story_id))
    return


def check_story(connection,root_path,story_id):
    """Process a single story given its ID number."""
    logging.info("Checking story "+repr(story_id))
    # Load API page for story
    api_url = "http://www.fimfiction.net/api/story.php?story="+str(story_id)
    raw_api_json = get(api_url)
    # Check if the story exists on the site
    api_dict = json.loads(raw_api_json)
    story_exists = check_if_story_exists(api_dict)
    if not story_exists:
        return
    # Determine if story has changed since last download
    remote_date_modified = api_dict["story"]["date_modified"]
    local_latest_version_number = find_newest_version(connection,story_id)
    if local_latest_version_number is None:
        new_version_number = 1
    else:
        new_version_number = local_latest_version_number + 1
        local_date_modified = lookup_date(connection,story_id,local_latest_version_number)
        if local_date_modified is None:
            local_date_modified = 0
        if (remote_date_modified <= local_date_modified):
            logging.info("Local version is up to date, no download needed.")
            return
    # If story has changed or is new, download it and add it to the DB
    save_story(connection,root_path,story_id,api_dict,raw_api_json,new_version_number)
    return


def check_range(connection,root_path,start_id,finish_id):
    """Process a range of stories"""
    logging.info("Checking range "+repr(start_id)+" to "+repr(finish_id))
    for story_id in xrange(start_id,finish_id):
        check_story(connection,root_path,story_id)
    logging.info("Finished checking range "+repr(start_id)+" to "+repr(finish_id))
    return


def main():
    try:
        setup_logging(log_file_path=os.path.join("debug","fimfic-dl-log.txt"))
        # Setup browser
        global cj
        cj = cookielib.LWPCookieJar()
        setup_browser(cj)
        connection = mysql.connector.connect(**config.sql_login)
        root_path = "download"
        check_story(connection,root_path,104188)

        check_range(connection,root_path,start_id=9,finish_id=1000)
        return
    except Exception, e:
        logging.critical("Unhandled exception!")
        logging.exception(e)
    logging.info("Finished, exiting.")
    return


if __name__ == '__main__':
    main()
