import io
import json
import codecs
import sys
from collections import defaultdict,Counter,Set

#Allows printing of unicode to windows terminal
# use print_to_stdout(userMessageMap.get(maxi[0]))
def print_to_stdout(*a):
 
    # Here a is the array holding the objects
    # passed as the argument of the function
    print(*a, file = sys.stdout)

#Generates map of users and the words they've used
def generateMap(path):
    userMessageMap = defaultdict()

    with open(path,encoding="utf-8") as f:
        data = json.load(f)
    sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
    

    for message in data["messages"]:
        user = message["author"]["name"]
        content = message["content"]

        if userMessageMap.get(user):
            userMessageMap[user] += content.split()
        else:
            userMessageMap[user] = content.split()
    return userMessageMap
def addToMap(path,userMessageMap):
    with open(path,encoding="utf-8") as f:
        data = json.load(f)    
    sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
    for message in data["messages"]:
        user = message["author"]["name"]
        content = message["content"]
    if userMessageMap.get(user):
        userMessageMap[user] += content.split()
    else:
        userMessageMap[user] = content.split()
    return userMessageMap
#Gets user with most words from map
def getTopKWords(userMessageMap, k):
    #needs to handle if k is negative or greater than total list?

    maxi = ["test",0]
    ans = []
    for key,value in userMessageMap.items():
        l = len(value)
        ans.append((key,l))
    sortedList = sorted(ans,key = lambda x:x[1])
    print(sortedList)
    return sortedList[k-1][0]
#Returns word frequency for a user
def getWordFrequency(user, map, doRemoveFiller):
    filler = []
    c = Counter(map.get(user))
    #Remove filler words
    if doRemoveFiller:
        my_file = open("CommonWords.txt", "r")
        content = my_file.read()
        contentList = content.split()
        for word in contentList:
            del c[word]
    #print(c)
    return c
#Shows words used by user1, not used by user2
def uniqueWords(user1,user2,map):
    set1 = set(map.get(user1))
    set2 = set(map.get(user2))
    print(set1 - set2)
def uniqueWordsInGroup(user1,map):
    set1 = set(map.get(user1))

    for key,val in map.items():
        if user1 != key:
            set1 = set1 - set(map.get(key))
    print(set1)
def mostUsedWordsByGroup(map,doRemoveFiller):
    filler = []
    c = None
    for user,val in map.items():
        if not c:
            c = Counter(map.get(user))
        else:
            c += Counter(map.get(user))
    #Remove filler words
    if doRemoveFiller:
        my_file = open("CommonWords.txt", "r")
        content = my_file.read()
        contentList = content.split()
        for word in contentList:
            del c[word]
            del c[word.capitalize()]
            del c[word[0] + word[1:]]
    #print(c)
    return c
#Returns user with most instances of a word
def playerWithMostWords(word,map):
    c = None
    maxi = 0
    userWithMostWords = ""
    for user,val in map.items():
        c = getWordFrequency(user,map,True)
        if c[word] > maxi:
            maxi = c[word]
            userWithMostWords = user
    print("User with most occurences of `" + word + "` is: " + userWithMostWords + " with " + str(maxi) + " occurences")
    return userWithMostWords
#Returns user with most instances of word as %% of their total word usage
def playerWithMostWordsPercent(word):
    pass

def userWithMostSwearWords(map):
    c = None
    userSwearCount = 0
    maxi = 0
    userWithMostSwears = ""

    my_file = open("SwearWords.txt", "r")
    content = my_file.read()
    swearList = content.split()

    temp = []
    temp2 = []
    for user,val in map.items():

        userSwearCount = 0
        listofSwears = []
        c = Counter(map.get(user))

        for word in swearList:
            if c[word] > 0:
                userSwearCount += c[word]
                listofSwears.append((word,c[word]))

        if userSwearCount > maxi:
            print("CHANGES")
            maxi = userSwearCount
            userWithMostSwears = user
            temp.append((userWithMostSwears,maxi))
            temp2.append( sorted(listofSwears,key = lambda x:x[1]))
    print(userWithMostSwears, maxi)
    print(temp)
    print(temp2[1])
    return userWithMostSwears

m = generateMap('Messages/general.json')
getTopKWords(m, 1)
#getWordFrequency("rayjones2170",m,True)
#uniqueWords("rayjones2170","CATHULULU",m)
#uniqueWordsInGroup("rayjones2170",m)
#mostUsedWordsByGroup(m,True)
playerWithMostWords("Ah", m)
userWithMostSwearWords(m)