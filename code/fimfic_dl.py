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


def check_story(story_id):
    """Process a single story given its ID number."""
    return





def check_range(start_id,finish_id):
    """Process a range of stories"""
    for story_id in xrange(start_id,finish_id):
        check_story(story_id)
    return



def main():
    try:
        setup_logging(log_file_path=os.path.join("debug","fimfic-dl-log.txt"))
        # Setup browser
        global cj
        cj = cookielib.LWPCookieJar()
        setup_browser(cj)
        check_range(start_id=0,finish_id=1000)
        return
    except Exception, e:
        logging.critical("Unhandled exception!")
        logging.exception(e)
    logging.info("Finished, exiting.")
    return


if __name__ == '__main__':
    main()
