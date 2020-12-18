from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
import pandas as pd
import demoji
from langdetect import detect
import re
from pathlib import Path, PureWindowsPath
import json
import os
from os.path import expanduser
from pathlib import Path
import googleapiclient.discovery
import json

class CommentStripper:


  def __init__(self,video_id,API_KEY):
    self.api_service_name = "youtube"
    self.api_version = "v3"
    self.DEVELOPER_KEY = API_KEY
    self.video_id = video_id
    self.youtube = googleapiclient.discovery.build(self.api_service_name,
                                                   self.api_version,
                                                   developerKey = self.DEVELOPER_KEY)
    self.count = 0

    self.video_title = None
    self.video_id_number = None
    self.channel = None
    self.channel_id = None
    self.video_likes = None
    self.video_dislikes = None
    self.video_view_count = None
    self.video_comment_count = None
    self.video_upload_time = None
    self.video_channel_subscribers = 105000000

    self.video_title_pop = []
    self.video_id_number_pop = []
    self.channel_pop = []
    self.channel_id_pop = []
    self.video_likes_pop = []
    self.video_dislikes_pop = []
    self.video_view_count_pop = []
    self.video_comment_count_pop = []
    self.video_upload_time_pop = []
    self.video_channel_subscribers_pop = []

    self.comment_id = []
    self.comment_string = []
    self.comment_likes = []
    self.comment_replies = []
    self.reply_comment = []
    self.parent_comment_id =[]
    self.parent_comment_string = []
    self.comment_channel_id = []
    self.comment_upload_time = []
    self.comment_channel_name = []

    self.comment_id_pop = []
    self.comment_string_pop = []
    self.comment_likes_pop = []
    self.comment_replies_pop = []
    self.reply_comment_pop = []
    self.parent_comment_id_pop =[]
    self.parent_comment_string_pop =[]
    self.comment_channel_id_pop = []
    self.comment_upload_time_pop = []
    self.comment_channel_name_pop = []

  def video_data(self):
    request = self.youtube.videos().list(
        part="snippet,contentDetails,statistics",
        id=self.video_id
    )
    video_data = request.execute()

    video_items = video_data["items"]
    self.video_title = video_items[0]['snippet']['title']
    self.video_id_number = video_items[0]['id']
    self.channel_id = video_items[0]['snippet']['channelId']
    self.channel = video_items[0]['snippet']['channelTitle']
    self.video_likes = video_items[0]['statistics']['likeCount']
    self.video_dislikes = video_items[0]['statistics']['dislikeCount']
    self.video_view_count = video_items[0]['statistics']['viewCount']
    self.video_comment_count = video_items[0]['statistics']['commentCount']
    self.video_upload_time = video_items[0]['snippet']['publishedAt']

  def top_comment_strip(self):
    nextPage_token = None
    while 1:
      request = self.youtube.commentThreads().list(
          part="snippet,replies",
          maxResults=100,
          order="time",
          pageToken= nextPage_token,
          textFormat="plainText",
          videoId= self.video_id
          )
      response = request.execute()
      nextPage_token = response.get('nextPageToken')

      for x in response["items"]:
        print("I am in top comment")
        self.count = self.count + 1
        print(self.count)

        try:
          self.comment_id_pop.append(x['snippet']['topLevelComment']['id'])
        except Exception as e:
          self.comment_id_pop.append('00000000')

        try:
          self.comment_string_pop.append(x['snippet']['topLevelComment']['snippet']['textDisplay'])
        except Exception as e:
          self.comment_string_pop.append('00000000')

        try:
          self.comment_likes_pop.append(x['snippet']['topLevelComment']['snippet']['likeCount'])
        except Exception as e:
          self.comment_likes_pop.append(0)

        try:
          self.comment_replies_pop.append(x['snippet']['totalReplyCount'])
        except Exception as e:
          self.comment_replies_pop.append('00000000')

        self.reply_comment_pop.append(False)

        try:
          self.parent_comment_id_pop.append(x['snippet']['topLevelComment']['id'])
        except Exception as e:
          self.parent_comment_id_pop.append('00000000')

        try:
          self.parent_comment_string_pop.append(x['snippet']['topLevelComment']['snippet']['textDisplay'])
        except Exception as e:
          self.parent_comment_string_pop.append('00000000')

        try:
          self.comment_channel_id_pop.append(x['snippet']['topLevelComment']['snippet']['authorChannelId']['value'])
        except Exception as e:
          self.comment_channel_id_pop.append('00000000')

        try:
         self.comment_upload_time_pop.append(x['snippet']['topLevelComment']['snippet']['publishedAt'])
        except Exception as e:
          self.comment_upload_time_pop.append("00000000")

        try:
          self.comment_channel_name_pop.append(x['snippet']['topLevelComment']['snippet']['authorDisplayName'])
        except Exception as e:
          self.comment_channel_name_pop.append('00000000')

        self.video_title_pop.append(self.video_title)
        self.video_id_number_pop.append(self.video_id_number)
        self.channel_pop.append(self.channel)
        self.channel_id_pop.append(self.channel_id)
        self.video_likes_pop.append(self.video_likes)
        self.video_dislikes_pop.append(self.video_dislikes)
        self.video_view_count_pop.append(self.video_view_count)
        self.video_comment_count_pop.append(self.video_comment_count)
        self.video_upload_time_pop.append(self.video_upload_time)
        self.video_channel_subscribers_pop.append(self.video_channel_subscribers)

        if x['snippet']['totalReplyCount'] > 0:
          self.reply_strip(x['snippet']['topLevelComment']['id'], x['snippet']['topLevelComment']['snippet']['textDisplay'])

      if nextPage_token is None:
        break

    output_dict = {
      "commentId": self.comment_id_pop,
      "commentString":self.comment_string_pop,
      "commentLikes":self.comment_likes_pop,
      "commentReplies":self.comment_replies_pop,
      "commentIsA_Reply":self.reply_comment_pop,
      "parentCommentId":self.parent_comment_id_pop,
      "parentCommentString":self.parent_comment_string_pop,
      "commentChannelId":self.comment_channel_id_pop,
      "commentUploadTime":self.comment_upload_time_pop,
      "commentChannelName":self.comment_channel_name_pop,
      "videoTitle":self.video_title_pop,
      "videoId":self.video_id_number_pop,
      "videoChannelTitle":self.channel_pop,
      "videoChannelID":self.channel_id_pop,
      "videoLikes":self.video_likes_pop,
      "videoDislikes":self.video_dislikes_pop,
      "videoViewCount":self.video_view_count_pop,
      "videoCommentCount":self.video_comment_count_pop,
      "videoUploadTime":self.video_upload_time_pop,
      "videoChannelSubscribers":self.video_channel_subscribers_pop
    }

    output_df = pd.DataFrame(output_dict, columns = output_dict.keys())

    return output_df

  def reply_strip(self,comment_id, comment_string):
    nextPage_token = None
    while 1:
      request = self.youtube.comments().list(
          part="snippet",
          maxResults=100,
          parentId=comment_id,
          pageToken=nextPage_token,
          textFormat="plainText"
          )
      replyList = request.execute()
      nextPage_token = replyList.get('nextPageToken')

      for item in replyList["items"]:
        print("I am in reply_strip")
        self.count = self.count + 1
        print(self.count)

        try:
            self.comment_id_pop.append(item['id'])
        except Exception as e:
            self.comment_id_pop.append('00000000')
        try:
            self.comment_string_pop.append(item['snippet']['textDisplay'])
        except Exception as e:
            self.comment_string_pop.append('00000000')
        try:
            self.comment_likes_pop.append(item['snippet']['likeCount'])
        except Exception as e:
             self.comment_likes_pop.append(0)

        self.comment_replies_pop.append(0)
        self.reply_comment_pop.append(True)

        try:
            self.parent_comment_id_pop.append(comment_id)
        except Exception as e:
            self.parent_comment_id_pop.append('00000000')
        try:
            self.parent_comment_string_pop.append(comment_string)
        except Exception as e:
            self.parent_comment_string_pop.append('00000000')
        try:
            self.comment_channel_id_pop.append(item['snippet']['authorChannelId']['value'])
        except Exception as e:
            self.comment_channel_id_pop.append('00000000')
        try:
            self.comment_upload_time_pop.append(item['snippet']['publishedAt'])
        except Exception as e:
            self.comment_upload_time_pop.append('00000000')
        try:
            self.comment_channel_name_pop.append(item['snippet']['authorDisplayName'])
        except Exception as e:
            self.comment_channel_name_pop.append('00000000')



        self.video_title_pop.append(self.video_title)
        self.video_id_number_pop.append(self.video_id_number)
        self.channel_pop.append(self.channel)
        self.channel_id_pop.append(self.channel_id)
        self.video_likes_pop.append(self.video_likes)
        self.video_dislikes_pop.append(self.video_dislikes)
        self.video_view_count_pop.append(self.video_view_count)
        self.video_comment_count_pop.append(self.video_comment_count)
        self.video_upload_time_pop.append(self.video_upload_time)
        self.video_channel_subscribers_pop.append(self.video_channel_subscribers)

      if nextPage_token is None:
        break


  def remove_unwanted(self,output_df):
    path_to_download_folder = expanduser("~") + '/Downloads'
    path_to_download_folder = path_to_download_folder + "/extraced.json"
    output_df.to_json(path_to_download_folder, orient = 'records')
    comments = pd.read_json(path_to_download_folder)
    demoji.download_codes()

    comments['clean_comments'] = comments['commentString'].apply(lambda x: demoji.replace(x,""))
    comments['language'] = 0

    comments['clean_parent_comments'] = comments['parentCommentString'].apply(lambda x: demoji.replace(x,""))
    comments['language'] = 0

    comments['clean_video_title'] = comments['videoTitle'].apply(lambda x: demoji.replace(x,""))
    comments['language'] = 0
    return comments

  def un_cringe(self,copy):
    path_to_download_folder = expanduser("~") + '/Downloads'
    path_to_download_folder = expanduser("~") + '/Downloads' + "/Dataset.json"
    regex = r"[^0-9A-Za-z'\t]"
    copy['reg'] = copy['clean_comments'].apply(lambda x:re.findall(regex,x))
    copy['theCommentString'] = copy['clean_comments'].apply(lambda x:re.sub(regex, " ",x))

    copy['reg'] = copy['clean_parent_comments'].apply(lambda x:re.findall(regex,x))
    copy['theParentCommentString'] = copy['clean_parent_comments'].apply(lambda x:re.sub(regex, " ",x))

    copy['reg'] = copy['clean_video_title'].apply(lambda x:re.findall(regex,x))
    copy['theVideoTitle'] = copy['clean_video_title'].apply(lambda x:re.sub(regex, " ",x))

    dataset = copy[['commentId','theCommentString','commentLikes','commentReplies','commentIsA_Reply','parentCommentId','theParentCommentString','commentChannelId','commentUploadTime', 'commentChannelName', 'theVideoTitle','videoId','videoChannelTitle','videoChannelID','videoLikes','videoDislikes','videoViewCount','videoCommentCount','videoUploadTime','videoChannelSubscribers']].copy()
    dataset.to_json(path_to_download_folder, orient = 'records' )


# In[19]:


#if __name__ == "__main__":
  #strip = CommentStripper("WwHmcuwrfCM")
  #strip.video_data()

  #x =strip.top_comment_strip()
  #y=strip.remove_unwanted(x)
  #strip.un_cringe(y)

  #with open("/Users/sriramgovindan/Desktop/Dataset.json", "r") as file:
      #json_file = json.load(file)

  #count = 0
  #max = 0
  #y = {}

  #for x in json_file:
      #if(x['commentLikes'] > max):
          #max = x['commentLikes']
          #y = x

  #print(y['commentLikes'], y['theCommentString'])
