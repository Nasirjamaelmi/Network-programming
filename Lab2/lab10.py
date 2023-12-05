import re

def task1():
    mtxt = "jox r.nohre@jth.hj.se, bjox@se, adam@example.com, jox@jox@jox.com."
    regex = r"(?:\s)[\w.]+@[\w]+\.[\w.]+"  #non capturing group med en space innan sen matchar jag med ord efter
    mails = re.findall(regex,mtxt)
    
    for email in mails:
        print("\t" + email)
    print("\n")

def task3():
    f = open("tabla.html", encoding="utf-8")
    txt = f.read()

    
    tid_regex = r"<td class=\"svtTablaTime\">\s*"  
    säsong_regex = r"(\d*\.\d*)\s+</td>\s+<td class=\"svtJsTablaShowInfo\">\s+<h4 class=\"svtLink-hover svtTablaHeading\">\s+"
    avsnitt_regex = r"Simpsons\s*</h4>\s*<div class=\"svtJsStopPropagation\">\s+<div class=\"svtTablaTitleInfo svtHide-Js\">\s+<div class=\"svtTablaContent-Description\">\s+"
    titel_regex = r"<p class=\"svtXMargin-Bottom-10px\">\s+Amerikansk animerad komediserie från [\d*]*\.\s*"
    desc_regex = r"Säsong (\d*)\. Del (\d*) av (\d+)\.(.*?)\s*</p>"
    
    serie = re.findall(f"{tid_regex}{säsong_regex}{avsnitt_regex}{titel_regex}{desc_regex}", txt)
    
    
    for ep in serie:
        print(f"|Tid\t|{ep[0]}\t|\n|-------|-------|\n|Säsong\t|{ep[1]}\t|\n|-------|-------|\n|Avsnitt|{ep[2]}/{ep[3]}\t|\n|-------|-------|\nHandling:{ep[4]}")
        print('_-_-' * 50 + "\n")

    
    
    

if __name__ == "__main__":
    #task1()
    task3()
    
#task 2 by using [] to match the words exatcly

