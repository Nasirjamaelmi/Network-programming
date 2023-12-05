name_points = {}

with open('score2.txt','r', encoding="utf-8") as f:
  for line in f:
     elements = line.split()
     firstnamn = elements[2]
     efternamn = elements[3]
     points = int(elements[4])

     name = f"{firstnamn} {efternamn}"
     
     if(name in name_points):
          name_points[name] += points
     else:
          name_points[name] = points
     
highest_score = max(name_points.values())


for student, points in name_points.items():
   if points == highest_score:
          print(f"{student} has the highest points {highest_score}")









#Maria Johansson has the highest points 37
#Kristina Larsson has the highest points 37




