__author__ = 'teo'
from bs4 import BeautifulSoup
import re
import requests
import itertools
import io #might be used to deal with ASCII problem
import sys

sys.setrecursionlimit(1073741824)
#Used for testing, to be replaced with IO system
start = "http://archiveofourown.org/works/search?utf8=%E2%9C%93&work_search[query]=&work_search[title]=&work_search[creator]=&work_search[revised_at]=&work_search[complete]=0&work_search[single_chapter]=0&work_search[word_count]=&work_search[language_id]=&work_search[fandom_names]=Homestuck%2CHarry+Potter+-+J.+K.+Rowling&work_search[rating_ids]=&work_search[character_names]=&work_search[relationship_names]=&work_search[freeform_names]=&work_search[hits]=&work_search[kudos_count]=&work_search[comments_count]=&work_search[bookmarks_count]=&work_search[sort_column]=&work_search[sort_direction]=&commit=Search"
start2 = "http://archiveofourown.org/works/search?commit=Search&page=4&utf8=%E2%9C%93&work_search[bookmarks_count]=&work_search[character_names]=&work_search[comments_count]=&work_search[complete]=0&work_search[creator]=&work_search[fandom_names]=Homestuck%2CHarry+Potter+-+J.+K.+Rowling&work_search[freeform_names]=&work_search[hits]=&work_search[kudos_count]=&work_search[language_id]=&work_search[query]=&work_search[rating_ids]=&work_search[relationship_names]=&work_search[revised_at]=&work_search[show_restricted]=false&work_search[single_chapter]=0&work_search[sort_column]=&work_search[sort_direction]=&work_search[title]=&work_search[word_count]="
r = requests.get(start)
a = r.text
soup = BeautifulSoup(a)
#print(soup.contents[1])


#Useful constants for parsing/printing that may change as AO3 does
standard_stat = ['Language:','Words:','Chapters:','Collections:','Comments:','Kudos:','Bookmarks:','Hits:'] #The names of the stats given in the stats section of a work blob
left_title = ['Title','Authors(s)','Fandom(s)'] #The names of all cols before the stats section
middle_title = ['Rating','Publication Date','Characters(s)','Relationship(s)','Warning(s)'] #The names of all cols after the states section, but before the free form tags

def link_to_soup(link):
    """Takes a link and returns the soup object for it"""
    r = requests.get(link)
    a = r.text
    soup = BeautifulSoup(a)
    return(soup)

def get_next_link(soup1):
    '''Takes the current soup from AO3 and gets the the link to the next page of search results; returns "None" if there is none'''
    a = soup1.find_all("li","next")
    b = a[0].a
    if (b==None):
        pass
        d = "None"
    else:
        add = 'http://archiveofourown.org'
        c = b.get('href')
        d = add + c
    return(d)

def get_all_soups(start):
    """Gets all bs4 objects for all the search pages from a serach"""
    soups = []
    soups.append(start)
    a = get_next_link(soups[-1])
    print(a)
    if (a != "None"):
        new_soup = link_to_soup(a)
        soups = soups + get_all_soups(new_soup)
    return(soups)

def contentPrint(soup):
    """Prints all the children of a soup with delimiters so that you can figure out what is what"""
    for x in range(0,len(soup.contents)):
        print(x,"===========================================================================")
        print(soup.contents[x])
        print(x,"===========================================================================")

def locationGet(soup1):
    """Gets the location of all the workblobs (i.e a works description)... unlikely to be changed, but easy to fix if it is"""
    soup2 = soup1.contents[1].contents[3].contents[1].contents[15].contents[7].contents[21]
    return(soup2)

def get_work_blobs(soup1):
    """Work blobs are located at all the odd children of the soup object with the workblobs. It will return a list of workblobs"""
    r = []
    for x in range(0,len(soup1.contents)):
        if (x % 2 != 0):
            r.append(soup1.contents[x])
        else:
            pass
    return(r)

def merger(ll):
    """Flattens a 2d list..."""
    return(list(itertools.chain(*ll)))


def kick_start(link1):
    """Given a search link, returns ALL of the work blobs for all pages of the search"""
    soup1 = link_to_soup(link1)
    print("We have all the links")
    soups = get_all_soups(soup1)
    print("We have all the soups")
    newsoups = []
    for x in range(0,len(soups)):
        print(x)
        newsoups.append(get_work_blobs(locationGet(soups[x])))
    blag = merger(newsoups)
    return (blag)



def info_compile(workb):
    """Takes a workblob and returns much of its metadata in a list format (which needs to be reformated"""
    title1 = title(workb)
    authors = author(workb)
    fandom = fandom_Get(workb)
    characters = character_List(workb)
    relationship = relationship_list(workb)
    warnings = warnings_List(workb)
    free = other_tags(workb)
    #work_status = work_Status(workb) Something isn't working here... needs to be looked into
    pdate = dateTime(workb)
    rating = rate(workb)
    stats = langWCKH(workb)
    statsr = langWCKH1(workb)
    rv = [title1,authors,fandom,stats,statsr,rating,pdate,characters,relationship,warnings, free]
    return(rv)


#This function is not being used everywhere it could be.... It is used to generalized all of the below functions...
def list_of_tags_to_string(temp1):
    """Takes a list of bs4 tags and gets their strings... because map wasnt working for some stupid bs4 reason... """
    #Look into the above
    r = []
    for x in range(0,len(temp1)):
        r.append(temp1[x].string)
    return(r)


def langWCKH(soup1):
    '''Gets the language, word count, chapter list, kudos, and hits from a work blab'''
    temp1 = soup1.find_all("dd")
    a = []
    for x in range(0,len(temp1)):
        a.append( temp1[x].string)
    return(a)

def langWCKH1(soup1):
    '''Gets if a work blob has the language, word count, chapter list, kudos, and hits from the work blab'''
    temp1 = soup1.find_all("dt")
    a = []
    for x in range(0,len(temp1)):
        a.append( temp1[x].string)
    return(a)

def fandom_Get(soup1):
    """Gets the fandom from the workblob"""
    temp1 = soup1.h5.find_all("a")
    r = []
    for x in range(0,len(temp1)):
        r.append(temp1[x].string)
    return (r)

def character_List(soup1):
    """Gets the character list from the workblob"""
    temp1 = soup1.find_all('li','characters')
    r = list_of_tags_to_string(temp1)
    return(r)

def warnings_List(soup1):
    """Gets the warnings list from the workblob"""
    temp1 = soup1.find_all('li',"warnings")
    r = list_of_tags_to_string(temp1)
    return(r)

def other_tags(soup1):
     """Gets the list of freeform tags from the workblob"""
     temp1 = soup1.find_all('li','freeforms')
     r = list_of_tags_to_string(temp1)
     return(r)

def relationship_list(soup1):
    """Gets the list of relationships from the workblob"""
    temp1 = soup1.find_all('li','relationships')
    r = list_of_tags_to_string(temp1)
    return(r)


def dateTime(sou1):
    """Gets the publication date and time"""
    return(sou1.find_all('p','datetime')[0].string)

def work_Status(soup1):
    """Gets if the work is complete, in-progress,etc"""
    return(soup1.find_all('span','complete-no iswip')[0].string)

def rate(soup1):
    """Gets the rating... M,General Audiance, etc"""
    return(soup1.find_all('span',re.compile('rating'))[0].string)


def author(soup1):
    """Gets the author from the workblob (Yes, I thought of this one last...)"""
    temp1 = soup1.h4.find_all('a','login author')
    r = list_of_tags_to_string(temp1)
    return(r)


def title(soup1):
    """Gets the title from the workblob"""
    temp1 = soup1.h4.a.string
    return(temp1)

def print_line(a):
    for x in range(0,len(a)):
        print(x,"============================================================================")
        print(a[x])
        print(x,"============================================================================")
#USE *************** MAP>>> WHAT IS IT WITH MAP AND BS4???????? AM I MAKING TYPOs everywhere?
def mapf(arg):
    """Mass applies getting info from to a list of workblobs """
    all_info = []
    for x in range(0,len(arg)):
        all_info.append(info_compile(arg[x]))
    return (all_info)

def list_diff(a, b):
    """A set dif function for lists i.e list_diff(a,b) =  a -b """
    new = []
    for x in range(0,len(a)):
        if (a[x] in b):
            pass
        elif (a[x] not in b):
            new.append(a[x])
    return(new)


def insertIndexes(a,b):
    """Inserts 0 in list a at all indexes in list b"""
    for x in range(0,len(b)):
        a.insert(b[x],0)
    return()

def stats_unfolder(record):
    """Takes the list of stats in the record created from a workblob and formates it in a csv print ready way"""
    first = record[0:3]
    #first[0] = '\"' + first[0] + '\"' #This exists to deal with the possibility of commas being in titles... this might need to be generalized to fields not handed by csv transformations
    inserts = record[3]
    if (isinstance(inserts[1],basestring)):
        inserts[1] = inserts[1].replace(',','') # -||-
    else:
        pass
    records = record[4]
    last = record[5:]
    if (len(record) ==  len(standard_stat)):
        return (first + inserts + last)
    else:
        diff = list_diff((standard_stat),(records))
        missInd = [standard_stat.index(x) for x in diff]
        insertIndexes(inserts,missInd)
        return (first + inserts + last)

#http://stackoverflow.com/questions/5655708/python-most-elegant-way-to-intersperse-a-list-with-an-element
def joinit(iterable, delimiter):
    it = iter(iterable)
    yield next(it)
    for x in it:
        yield delimiter
        yield x

def csv_sub_transform(record,a):
    """Takes a record, an index of that record, which should correspond to a list. Intersparses the list with commas, concats it, and then encloses it in commas to avoid upsetting the csv standards"""
    record[a] = '\"' + (','.join(record[a])) + '\"'
    return ()

def csv_transformer(record):
    """Mass applies csv transform to all indexes corresponding to lists, but the last index of the record."""
    for x in range(0,(len(record) -1)):
        #if isinstance(record[x],basestring):
            #record[x] = '\"' + record[x] + '\"'
        if isinstance(record[x],list):
            csv_sub_transform(record,x)
        else:
            pass


#Probably about as inefficient as possible....
def nub(x):
    """Deletes all duplicates from a list"""
    new = []
    new .append(x[0])
    for x1 in range(1,len(x)):
        if (x[x1] in new):
            pass
        if (x[x1] not in new):
            new.append(x[x1])
    return(new)

def col_collection(records):
    """Takes the collection of records and returns the list of freeform tags."""
    z = len(records[0]) - 1
    a = records[0][z]
    #rewrite!
    for x in range(1,len(records)):
        print(x)
        z1 = len(records[x]) -1
        a = a + records[x][z1]
    return(list(set(a))) #list/set/


def tags_to_colums(data,x,col):
    """Replaces the list of freeform tags in a record with a list of 0 and 1s were the 1s are where the record's free form tags are in the list of overall tags...  """
    #Come up with a better exp?
    lcol = len(col)
    template_list = [0]*lcol
    if data[x] != []:
        for x1 in range(0,len(data[x])):
            a = col.index(data[x][x1])
            template_list[a] = 1
    data[x] = template_list



def csv_write(l):
    """Prepares the list of details from a record for printing into a csv"""
    #print(l)
    #l_1= map(str,l)
    l_1 = []
    for x in range(0,len(l)):
        #print(x)
        if isinstance(l[x],int):
            l[x] = str(l[x])
        l_1.append((l[x].encode('utf-8')))
        #print_line(l[x])
    return((','.join(l_1)) + '\n')

def double_qoutes_fixer(record):
    if (record[0].count('\"')) == 4:
        record[0] = record[0][1:]
        record[0] = record[0][:-1]
    else:
        pass

def link_to_csv(start_link):
    """Requires some explanations"""
    a = kick_start(start_link)
    b = mapf(a)
    #print(len(b))
    col = col_collection(b) #rewrite to go for the last one... also... fucking hell can we figure out what is going on in stats (again???)
    print('Coled!')
   # print(b[6])
    for x in range(0,len(b)):
        b[x] = stats_unfolder(b[x])
        csv_transformer(b[x])
        tags_to_colums(b[x],(len(b[x])-1),col)
        b[x][0] = '\"' + b[x][0] + '\"'
        double_qoutes_fixer(b[x])
        a = b[x].pop()
        b[x] = b[x] + a
        print(x)
    title = left_title + standard_stat + middle_title + col
    #print(len(title))
    #print(csv_write(b[0]))
    csv = open('data.csv','w')
    csv.write(csv_write(title))
    #print(b[32])
    #g.append( (b[33][3]))
    #print(g)
    for x1 in range(0,len(b)):
        print('gag',x1)
        csv.write(csv_write(b[x1]))
        #print(csv_write(b[x1]))
        #print(b[x1])
    csv.close()

def main():
    link = input("Input the link to the first page of your archive of our own search (in qoutes):")
    print(link)
    link_to_csv(link)
    print('Done!')

main()
#http://archiveofourown.org/works/search?utf8=%E2%9C%93&work_search[query]=&work_search[title]=&work_search[creator]=&work_search[revised_at]=&work_search[complete]=0&work_search[single_chapter]=0&work_search[word_count]=&work_search[language_id]=&work_search[fandom_names]=&work_search[rating_ids]=13&work_search[warning_ids][]=19&work_search[category_ids][]=116&work_search[character_names]=&work_search[relationship_names]=&work_search[freeform_names]=&work_search[hits]=&work_search[kudos_count]=&work_search[comments_count]=&work_search[bookmarks_count]=&work_search[sort_column]=&work_search[sort_direction]=&commit=Search