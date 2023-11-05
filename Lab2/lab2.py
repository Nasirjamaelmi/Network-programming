f = open('Lab2\score2.txt', 'r', encoding="utf-8")
name_points = {}

for line in f:
   
   elements = line.split()
   
   firstnamn = elements[2]
   efternamn = elements[3]
   points = elements[4]

   name = f"{firstnamn} {efternamn}"
   
   if(name in name_points):
        name_points[name] += int(points)
   else:
       name_points[name] = int(points)



