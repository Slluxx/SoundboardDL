import argparse, requests, os, re
from urllib.parse import urlparse

def process(url):
    try:
        boardName = str(url.path.replace("/sb/", "").replace("/", ""))
        jsonUrl = "https://www.soundboard.com/handler/gettrackjson.ashx?boardname=" + boardName
        json_object = requests.get(jsonUrl).json()

        # create folder if it doesn't exist
        if not os.path.exists(boardName):
            os.makedirs(boardName)

        # download files into folder
        for track in json_object:
            title = re.sub('[^0-9a-zA-Z]_', '-', track["title"].strip()
                .replace("*", "-").replace(" ", "_").replace("?", "").replace("'", "").replace("(", "").replace(")", ""))
            file_extension = os.path.splitext(track["mp3"])[1]

            # if file already exists, skip
            file_path = os.path.join(os.getcwd(), boardName, title + file_extension)
            if os.path.isfile(file_path):
                print("File already exists, skipping. " + file_path)
                continue
            else:
                print("Downloading file: " + title)
                with open(file_path, "wb") as file:
                    response = requests.get(track["mp3"])
                    file.write(response.content)
                    print("File downloaded successfully!")



    except Exception as e:
        print("Error: " + str(e))
        exit(1)


parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", type=str, help="URL to a soundboard.com page. EG: https://www.soundboard.com/sb/starwars")
args = parser.parse_args()

if args.url:
    url = urlparse(args.url)
    process(url)
else:
    print("Please enter a URL to a soundboard.com page. EG: https://www.soundboard.com/sb/starwars\n")
    url = urlparse(input("URL: "))
    process(url)
    input("Done. Press a key to exit...")
