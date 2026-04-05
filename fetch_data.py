# =========================================
# IMPORT LIBRARIES
# =========================================
from googleapiclient.discovery import build
import pandas as pd
from datetime import datetime
from config import API_KEY

print("DEBUG API KEY:", API_KEY)

if not API_KEY:
    print("❌ API KEY NOT FOUND")
    exit()
# =========================================
# CONNECT TO YOUTUBE API
# =========================================
youtube = build('youtube', 'v3', developerKey=API_KEY)

# =========================================
# FETCH FUNCTION
# =========================================
def fetch_data():
    request = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        regionCode="IN",
        maxResults=50
    )

    response = request.execute()

    data = []

    for item in response['items']:
        video = {
            'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'title': item['snippet']['title'],
            'channel': item['snippet']['channelTitle'],
            'views': int(item['statistics'].get('viewCount', 0)),
            'likes': int(item['statistics'].get('likeCount', 0)),
            'comments': int(item['statistics'].get('commentCount', 0))
        }
        data.append(video)

    return pd.DataFrame(data)

# =========================================
# SAVE DATA (AUTO UPDATE LOGIC)
# =========================================
if __name__ == "__main__":
    df = fetch_data()

    try:
        old_df = pd.read_csv("youtube_data.csv")
        df = pd.concat([old_df, df], ignore_index=True)
    except:
        pass

    df.to_csv("youtube_data.csv", index=False)
    print("Data Updated Successfully!")