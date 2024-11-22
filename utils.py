from gui import DIR_NAME


def generate_delta(path, version_new):
    """
    Function to generate delta from a new database version
    """
    BASE_VER = 1
    filename = str(path.split('/')[1])
    DIR_NAME = str(path.split('/')[0])

    if(version_new == BASE_VER):

        # A new database is being added
        git_message = "Added version " + str(version_new) + \
            " of the " + filename + " in " + DIR_NAME + " database"

        return(path, git_message)

    else:

        CURR_VER = version_new - 1
        if(CURR_VER == 1):
            # Current version is base version. Generate delta using base version of database
            print('Current is Base')
            # Fetch database for BASE version

            #DELTA = NEW_VERSION - BASE_VERSION

            git_message = "Added version " + str(version_new) + \
                " of the " + filename + " in " + DIR_NAME + " database"

        else:
            # Fetch delta
            print('Fetch Delta')
            # Fetch database for CURRENT version

            #DELTA = NEW_VERSION - CURRENT_VERSION

            git_message = "Added delta version " + str(version_new) + \
                " of the " + filename + " in " + DIR_NAME + " database"
