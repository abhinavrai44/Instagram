#!/usr/bin/env python
import argparse
from bs4 import BeautifulSoup
import urllib2 as urllib
import json

parser = argparse.ArgumentParser(description='scrap instagram')
parser.add_argument('username', type=str,
                    help='an integer for the accumulator')

args = parser.parse_args()

username = args.username

base_url = "https://www.instagram.com/"
pages = 0
maxlikes = maxComments = -1
minlikes = minComments = 100000000000
maxLiID = maxCoID = -1

comments = likes = retrievedPosts = 0

url = base_url + username
while 1:

	pages = pages + 1
	
	# print(url)
	req = urllib.Request(
	url, 
	data=None, 
	headers={
	    'User-Agent': 'Mozilla/47.0'
	}
	)

	try:
		page = urllib.urlopen(req)
		# page = urlopen(url)
		soup = BeautifulSoup(page)
		json_ = soup.findAll("script")
		string = json_[6].text[21:-1]

		dObj = json.loads(string)
		# strD = json.dumps(dObj,indent=4)
		# print(strD)
		# break
									# to be removed 
		user = dObj["entry_data"]["ProfilePage"][0]["user"]
		following = user["follows"]["count"]
		followers = user["followed_by"]["count"]
		cursorData = user["media"]["page_info"]
		max_id = cursorData["end_cursor"]

		posts = user["media"]
		totalPosts = posts["count"]
		strData = json.dumps(cursorData,indent=4)

		for post in posts["nodes"]:
			retrievedPosts += 1
			if maxlikes < post["likes"]["count"]:
				maxLiID = post["id"]
				maxlikes = post["likes"]["count"]

			if minlikes > post["likes"]["count"]:
				minlikes = post["likes"]["count"]

			if maxComments < post["comments"]["count"]:
				maxCoID = post["id"]
				maxComments = post["comments"]["count"]

			if minComments > post["comments"]["count"]:
				minComments = post["comments"]["count"]

			comments += post["comments"]["count"]
			likes += post["likes"]["count"]

		if(cursorData["has_next_page"]	and pages<3):
			url = base_url + username + "/?max_id=" + max_id
		else:
			break
			
	except:
		pass


userObj = {}
userObj["following"] = following
userObj["followers"] = followers
userObj["totalPosts"] = totalPosts
userObj["retrievedPosts"] = retrievedPosts
userObj["comments"] = comments
userObj["likes"] = likes
userObj["avgLikes"] = likes/retrievedPosts
userObj["avgComments"] = comments/retrievedPosts
userObj["maxComments"] = maxComments
userObj["maxlikes"] = maxlikes
userObj["minComments"] = minComments
userObj["minlikes"] = minlikes
userObj["maxLikesID"] = maxLiID
userObj["maxCommentsID"] = maxCoID
strData = json.dumps(userObj)

print(strData)


	
