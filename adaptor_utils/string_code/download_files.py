import os.path
import wget


def download_db(url, directory):
    try:
        file_name = url.split('/')[-1]
        # downloading the files
        if not os.path.exists(os.path.join(directory, file_name)):
            print("Downloading", url)
            wget.download(url, os.path.join(directory, file_name))

    except Exception as err:
        raise Exception("Something went wrong. {}.\nURL:{}".format(err, url))

    return file_name
