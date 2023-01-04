# import libraries
import requests
import pandas as pd

# make api call
def call_api(api_key, channel_id):
    pageToken = ""
    url = 'https://www.googleapis.com/youtube/v3/search?key='+api_key+'&channelId='+channel_id+'&part=snippet,id&order=date&maxResults=10000'+pageToken
    response = requests.get(url).json()
    return response

# get details of a video
def get_video_details(video_id):
    # make api call for like, view, comments
    url_video_stats = 'https://www.googleapis.com/youtube/v3/videos?id='+video_id+'&part=statistics&key='+api_key
    response_video_stats = requests.get(url_video_stats).json()
    # make api call for video duration
    url_video_dur = 'https://www.googleapis.com/youtube/v3/videos?id='+video_id+'&part=contentDetails&key='+api_key
    response_video_dur = requests.get(url_video_dur).json()
    # make api call for video tags
    url_video_tags = 'https://www.googleapis.com/youtube/v3/videos?id='+video_id+'&part=snippet&key='+api_key
    response_video_tags = requests.get(url_video_tags).json()  

    if 'viewCount' in response_video_stats['items'][0]['statistics']:
        view_count = response_video_stats['items'][0]['statistics']['viewCount']
    else:
        view_count = 0
    if 'likeCount' in response_video_stats['items'][0]['statistics']:
        like_count = response_video_stats['items'][0]['statistics']['likeCount']
    else:
        like_count = 0
    if 'dislikeCount' in response_video_stats['items'][0]['statistics']:
        dislike_count = response_video_stats['items'][0]['statistics']['dislikeCount']
    else:
        dislike_count = 0
    if 'commentCount' in response_video_stats['items'][0]['statistics']:
        comment_count = response_video_stats['items'][0]['statistics']['commentCount']
    else:
        comment_count = 0
    if 'duration' in response_video_dur["items"][0]["contentDetails"]:
        duration = response_video_dur["items"][0]["contentDetails"]["duration"]
    else:
        duration = 0
    if 'tags' in response_video_tags["items"][0]["snippet"]:
        tags = response_video_tags["items"][0]["snippet"]["tags"]
    else:
        tags = []
    
    return view_count, like_count, dislike_count, comment_count, duration, tags

# get all the videos of a channel
def get_videos(response, df):
    for video in response['items']:
        if video['id']['kind'] == 'youtube#video':
            video_id = video['id']['videoId']
            video_title = video['snippet']['title']
            video_title = video_title.replace("&amp;", "")
            upload_date = video['snippet']['publishTime']
            upload_date = upload_date.split("T")[0]
            
            view_count, like_count, dislike_count, comment_count, duration, tags = get_video_details(video_id)

            #save data in pandas dataframe
            df = df.append({'video_id':video_id, 'video_title':video_title,
                            'upload_date':upload_date, 'view_count':view_count,
                            'like_count':like_count, 'dislike_count':dislike_count,
                            'comment_count':comment_count, 'duration':duration,
                            'tags':tags}, ignore_index=True)
    df['upload_date'] = df['upload_date'] = pd.to_datetime(df['upload_date'])
    return df

df = pd.DataFrame(columns=["video_id", "video_title", "upload_date", "view_count", "like_count", "dislike_count", "comment_count"])