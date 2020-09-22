from secrets import * 
import tweepy
import time

# Identificacion #
auth = tweepy.OAuthHandler(C_KEY, C_SECRET)  
auth.set_access_token(A_TOKEN, A_TOKEN_SECRET)  
api = tweepy.API(auth) 

def getID (lista):
    return lista._json['id']

def getIDlist(lista):
    return [getID(i) for i in lista]

mostRecentId = None

while True:
    try:
        mostRecentId = getID(list(api.mentions_timeline(count=1,tweet_mode = 'extended'))[0])
        break
    except Exception as e:
        print("Error getting most recent messages, trying again in 10 seconds")
        time.sleep(20)

ignoreList = [mostRecentId]

while True:
    print("Sleeping 10 seconds")
    time.sleep(30)
    print("Not sleeping anymore. MostRecentId: ",mostRecentId)
    mentionsList = None
    try:
        mentionsList = list(api.mentions_timeline(since_id = mostRecentId, count = 10, tweet_mode = 'extended'))
        print("MentionsList: ", mentionsList)
        if len(mentionsList) > 0:
            pass
        else: #No new tweets
            continue
    except Exception as e:
        print("Error getting total timeline: ",e)
        time.sleep(20)
        continue
    if len(mentionsList) > 0:
        mostRecentId = getID(mentionsList[0])
        #actualList = [t for t in mentionsList if getID(t) not in ignoreList] # To eliminate duplicates
        actualList = [t for t in mentionsList] # By now I don't need to ignore duplicates, I don't expect that much stream
        ignoreList.extend(getIDlist(actualList))

        if len(actualList)==0: continue
        
        #answeringTo = None
        for actualTweet in actualList:
            try:
                print("Esto que es: ",actualTweet)
                answeringTo = api.get_status(actualTweet._json['in_reply_to_status_id_str'],tweet_mode='extended')
                print (answeringTo)
                if(answeringTo != None):
                    media_list = []
                    response = api.media_upload("./DAMN_GIF_BOT.gif")
                    media_list.append(response.media_id_string)
                    api.update_status("DAAAAAMN!!!",in_reply_to_status_id = actualTweet._json['in_reply_to_status_id_str'],auto_populate_reply_metadata=True, media_ids = media_list)
            except tweepy.TweepError as E:
                print("Error: ",E)
    

        #print(answeringTo)
    
    