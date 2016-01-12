AO3-Data-Collector
==================
Purpose
------------------
This program will take an archiveofourown search and return useful statistics for all the works in a csv. What makes this one particularly special? This one focuses on getting all tag related into a very convient form. Specifically, for each tag it encounters it will add a column to the dataset where 1 means the work had the tag and 0 means that it did not. This will make it much easier for most people to analyze relationships involving tag and it make testing how tag wrangling is doing much easier. 
Problems
------------------
This approach has two problems. 

One, it is really memory intensive/slow. This is why I'm buidling a c version with libcurl + libxml because there is probably no faster way of doing anything related to the web or anything related to html (and no one yet understands why libxml does what it does so fast). Additionally, I could refactor the python code to use numpy, but I'm kind of skeptical that this will deal with the memory problem. 

The second issue is demonstrated by "why you should use r".png. The solution is for everyone to use R, but it is kind of sad because I wanted this to be easy to use.

##To do list##
0. Rewrite it all in C.
1. Add user input for file names.
2. Tests. Lots of tests. 
3. Rewrite all the docstrings in a more useful manner... 
4. Deal with a problem involving map and bs4 objects that might just be in my imagination... 
5. Add useful information about how this works in the README.
