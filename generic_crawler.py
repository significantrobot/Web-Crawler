"""
Function Name: search_dict
Input: dictionary
Output:
Function Operation:
  This function searches the dictionary
  for a key (user input) and prints
  the associated values
"""


def search_dict(content):
    key_to_isolate = input("enter file name:\n")
    if key_to_isolate not in content:
        print("File not found.")
    elif key_to_isolate in content:
        if content[key_to_isolate] != None:
            print(content[key_to_isolate])
        else:
            #If file in question had no links
            print("[]")

            
"""
Function Name: create_CSV
Input: dictionary
Output:
Function Operation:
  This function creates a CSV file
  out of the dictinoary.
"""



def create_CSV(content):
    file = open("results.csv", "w+")
    for key, value in content.items():
        ##Writes the key
        file.write(str(key))
        if value == None:
            file.write("\n")
        elif value != None:
            ## Writes the values
            file.write(",")
            num_of_values = len(value)
            i = 0
            while i < num_of_values:
                file.write(str(value[i]))
                if i != num_of_values - 1:
                    file.write(",")
                if i == num_of_values - 1:
                    file.write("\n")
                i = i + 1
    file.close()


"""
Function Name: insertion
Input: str link_from, str link_to, dictionary
Output:
Function Operation:
  This function inserts a key and value to the dictionary
"""


def insertion(link_from, link_to, content):
    content[link_from] = link_to


"""
Function Name: parser
Input: str plain_text, dictionary
Output: List
Function Operation:
  This function parses plain_text down to only
  the name of the html file linked to in the source.
  Returns a list containing the names of all the html files
  linked to in the source
"""


def parser(plain_text, content):
    default_list = []
    if "<a href=" in plain_text:
        ##whittling text down to names of linked files
        step_0 = plain_text.split("<a href=")
        max_links = plain_text.count("<a href=")
        i = 1
        while i<max_links + 1:
            html_excerpt = step_0[i]
            html_excerpt = html_excerpt.split(">")[0]
            html_excerpt = html_excerpt.split("\"")[1]
            ##inserting name of linked file to list
            default_list.append(html_excerpt)
            i = i + 1
        ##sorting the list in ascending order
        default_list.sort()
        ##returning the list
        return default_list
    else:
        ##If the file contains no links
        return None


"""
Function Name: spider
Input: str start_page, dictionary
Output:
Function Operation:
  This function turns the html source file
  into a string, which it sends to parser.
  It then sends the list returned by parser
  to the insertion function, which inserts it
  as a value in the dictionary
"""


   
def spider(start_page, content):
    ##checking if the page has already been mined
    if start_page not in content.keys():
        try:
            ##converting html into string
            with open(start_page) as file_to_read:
                plain_text = file_to_read.read()
                link_list = parser(plain_text, content)
                insertion(start_page, link_list, content)
                i = 0
                try:
                    ##recursion into next file
                    while i < len(link_list):
                        spider(link_list[i], content)
                        i = i + 1
                ##if the current file has no links
                except TypeError:
                    pass
        ##if source file input is invalid
        except FileNotFoundError:
            return
    else:
        return
        
        
##initializing the dictionary
content = {}
##user inputs source file
start_page = input("enter source file:\n")
spider(start_page, content)
##creating CSV file
create_CSV(content)
##searching dictionary
search_dict(content)
