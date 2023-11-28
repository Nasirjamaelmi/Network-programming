import re
txt = "Hanoror bought 5 portions of orange soil for 13.50 EUR."
re.findall("or", txt)  #regex is used to manipulate txt to get wanted result in this exempel we get or
re.findall(".", txt) #matches all characthers
re.findall( "or.", txt) #matches with or and any charachter after
re.findall("..\.", txt) # i get 2 characthers who has a dot after
print("Hello\nWorld") # it interpret it as a new line with \n
print(r"Hello\nWorld") # it write the whole as a string with \n
re.findall(r"\w", txt) #Matches all characther almost
re.findall(r"\W", txt) #matches all non characther the opposite
re.findall(r"\d", txt) #d as digit matches all digits
re.findall(r"\D", txt) #matches all characther
re.findall(r"\s", txt) #s as in space ('\n', '\r', '\t')
re.findall(r"\S", txt) # all chars

