##Archery Score Manager

from packer import packer
import datetime, time, csv

#p = packer("archery.jpk")

## Data Structure:
##  [Bow, Date Tuple, Round, Final Score, Shots List, Class, Handicap]

def cls():
    print "\n"*100
    
door = ""
while (door != "I") and (door != "O"):
    door = raw_input("(I)ndoor or (O)utdoor? ").upper()
if door == "I":
    p = packer("indoor.jpk")
if door == "O":
    p = packer("outdoor.jpk")

def int_input(prompt):
    while 1:
        try:
            x = int(raw_input(prompt))
            break
        except ValueError:
            continue
    return x
    
def add_round(bow,date,Round,final_score,shots,classification,handicap):
    p.write_array([bow.lower(),date,Round.lower(),final_score,shots,str(classification).lower(),handicap])
    print "Added!"

def add_round_menu():
    datestr = raw_input("Enter date (DD/MM/YYYY)... ")
    date = time.mktime(datetime.datetime.strptime(datestr,"%d/%m/%Y").timetuple())
    bow_type = raw_input("Enter bow type... ").lower()
    round_name = raw_input("Enter name of round... ").lower()
    final_score = int_input("Enter final score... ")
    shots = []
    for x in range(int_input("Enter number of ends... ")):
        length = 0
        while length != 6:
            end = raw_input("Enter shots for end "+str(x+1)+"... ").upper()
            end = end.replace("M","0")
            def sort(val):
                if val == "X":
                    return 11
                else:
                    return int(val)
            end = end.split(" ")
            for val in end:
                try:
                    end[end.index(val)] = int(val)
                except:
                    pass
            end = sorted(end,reverse=True,key=sort)
            length = len(end)
        shots += end
    if sum([int(y) for y in ((" ".join([str(x) for x in shots]).replace("X","10")).split(" "))]) != final_score:
        raise ValueError("sum of shots is not equal to final score!")
    classification = raw_input("Enter class... ").lower()
    handicap = int_input("Enter handicap... ")
    print
    print "Bow: "+bow_type
    print "Date: "+datestr
    print "Round: "+round_name
    print "Score: "+str(final_score)
    print "Class: "+classification
    print "Handicap: "+str(handicap)
    print "--Shots--"
    strshots = [str(x) for x in shots]
    for x in range(len(shots)/6):
        print ", ".join(strshots[x*6:(x+1)*6])
    print "\nIs that correct?"
    choice = ""
    while (choice != "Y") and (choice != "N"):
        choice = raw_input("(Y/N)? ").upper()
    if choice == "Y":
        add_round(bow_type,date,round_name,final_score,shots,classification,handicap)
        print
        return 0
    else:
        print
        return 1
def output_rounds(data):
    for x in range(len(data)):
        r = data[x]
        print "\n  -- "+str(x)+" --"
        print "Bow: "+r[0]
        print "Date: "+datetime.datetime.fromtimestamp(r[1]).strftime("%d/%m/%Y")
        print "Round: "+r[2]
        print "Score: "+str(r[3])
        print "Class: "+r[5]
        print "Handicap: "+str(r[6])
        print "--Shots--"
        strshots = [str(y) for y in r[4]]
        for y in range(len(strshots)/6):
            print ", ".join(strshots[y*6:(y+1)*6])
        print

def compact_output(data):
    print "\n  id  ||   bow   ||   Date   ||    Round    || Score || Class || Handicap"
    for y in range(len(data)):
        stry = str(y)
        x = data[y]
        x = [str(y) for y in x]
        while len(stry) < 6:
            stry+= " "
        while len(str(x[0])) < 9:
            x[0] += " "
        while len(str(x[1])) < 10:
            x[1] += " "
        while len(str(x[2])) < 13:
            x[2] += " "
        while len(str(x[3])) < 7:
            x[3] += " "
        while len(str(x[5])) < 7:
            x[5] += " "
        print stry+"||"+x[0]+"||"+x[1]+"||"+x[2]+"||"+x[3]+"||"+x[5]+"||"+x[6]
    print
def view_round_menu(compact=False):
    print "0) View all"
    print "1) View score by date"
    print "2) View score by round"
    print "3) View score by bow"
    print "4) View score by classification achieved"
    print "i) View score by id"
    print "q) Cancel"
    while 1:
        choice = raw_input("Enter selection... ").lower()
        if choice == "q":
            return 0
        elif choice == "i":
            i = int_input("Enter id... ")
            data = p.read(i)
            if compact:
                compact_output([data])
            else:
                output_rounds([data])
        elif (int(choice) >= 0) and (int(choice) < 5):
            break
    if choice == "0":
        if compact:
            compact_output(p.read())
        else:
            output_rounds(p.read())
    if choice == "1":
        datestr = raw_input("Enter date (DD/MM/YYYY)... ")
        date = time.mktime(datetime.datetime.strptime(datestr,"%d/%m/%Y").timetuple())
        data = [x for x in p.read() if x[1] == date]
        if compact:
            compact_output(data)
        else:
            output_rounds(data)
    if choice == "2":
        name = raw_input("Enter round name... ").lower()
        data = [x for x in p.read() if x[2] == name]
        if compact:
            compact_output(data)
        else:
            output_rounds(data)
    if choice == "3":
        bow = raw_input("Enter bow... ").lower()
        data = [x for x in p.read() if x[0] == bow]
        if compact:
            compact_output(data)
        else:
            output_rounds(data)
    if choice == "4":
        classification = raw_input("Enter class... ").lower()
        data = [x for x in p.read() if x[5] == classification]
        if compact:
            compact_output(data)
        else:
            output_rounds(data)

def average_menu():
    bow = raw_input("Make target for which bow? ").lower()
    data = [x for x in p.read() if x[0] == bow]
    nums = [0,0,0,0,0,0,0,0,0,0,0,0]
    for x in data:
        for y in x[4]:
            if y == "X":
                nums[10] += 1
            else:
                nums[int(y)] += 1
    total_shots = sum(nums)
    probability = [
        nums[0]/float(total_shots),
        nums[1]/float(total_shots),
        nums[2]/float(total_shots),
        nums[3]/float(total_shots),
        nums[4]/float(total_shots),
        nums[5]/float(total_shots),
        nums[6]/float(total_shots),
        nums[7]/float(total_shots),
        nums[8]/float(total_shots),
        nums[9]/float(total_shots),
        nums[10]/float(total_shots)]
    ends = int_input("How many ends? ")
    average = 0*probability[0]+\
              1*probability[1]+\
              2*probability[2]+\
              3*probability[3]+\
              4*probability[4]+\
              5*probability[5]+\
              6*probability[6]+\
              7*probability[7]+\
              8*probability[8]+\
              9*probability[9]+\
              10*probability[10]
    average_squared = (0**2)*probability[0]+\
                      (1**2)*probability[1]+\
                      (2**2)*probability[2]+\
                      (3**2)*probability[3]+\
                      (4**2)*probability[4]+\
                      (5**2)*probability[5]+\
                      (6**2)*probability[6]+\
                      (7**2)*probability[7]+\
                      (8**2)*probability[8]+\
                      (9**2)*probability[9]+\
                      (10**2)*probability[10]
                      
    print "\nDistribution:"
    print "-M-   -1-   -2-   -3-   -4-   -5-   -6-   -7-   -8-   -9-   -10-"
    print ", ".join([str(round(x,2)) for x in probability]),"\n"
    print "Your expected score per arrow is "+str(round(average,2))
    print "Your standard deviation is "+str(round((average_squared-(average**2))**0.5,2))
    print "Your target is "+str(round(average*(ends*6),2))

def csv_menu():
    filename = raw_input("Enter file to export to... ")
    f = open(filename,"wb")
    writer = csv.writer(f)
    writer.writerow(['Bow', 'Date', 'Round', 'Final Score', 'Class', 'Handicap'])
    data = p.read()
    for x in range(len(data)):
        data[x].pop(4)
        data[x][1] = datetime.datetime.fromtimestamp(data[x][1]).strftime("%d/%m/%Y")
    for d in data:
        writer.writerow(d)
    f.close()
    print "Written!"
              
        

### --Interface Code Here!-- ###

while 1:
    print
    print "1) Add score"
    print "2) View scores"
    print "3) View scores (compact)"
    print "4) Calculate target"
    print "5) Export CSV"
    print "q) Quit"


    choice = raw_input("Enter selection... ").lower()
    if choice == "1":
        #cls()
        print
        try:
            code = add_round_menu()
        except KeyboardInterrupt:
            code = 1
        while code:
            print "Quit?"
            choice = ""
            while (choice != "Y") and (choice != "N"):
                choice = raw_input("(Y/N)? ").upper()
            if choice == "Y":
                break
            else:
                try:
                    code = add_round_menu()
                except KeyboardInterrupt:
                    code = 1
    elif choice == "2":
        print
        try:
            code = view_round_menu()
        except KeyboardInterrupt:
            code = 1
        while code:
            print "Quit?"
            choice = ""
            while (choice != "Y") and (choice != "N"):
                choice = raw_input("(Y/N)? ").upper()
            if choice == "Y":
                break
            else:
                try:
                    code = view_round_menu()
                except KeyboardInterrupt:
                    code = 1
    elif choice == "3":
        print
        try:
            code = view_round_menu(True)
        except KeyboardInterrupt:
            code = 1
        while code:
            print "Quit?"
            choice = ""
            while (choice != "Y") and (choice != "N"):
                choice = raw_input("(Y/N)? ").upper()
            if choice == "Y":
                break
            else:
                try:
                    code = view_round_menu(True)
                except KeyboardInterrupt:
                    code = 1
    elif choice == "4":
        print
        try:
            code = average_menu()
        except KeyboardInterrupt:
            code = 1
        while code:
            print "Quit?"
            choice = ""
            while (choice != "Y") and (choice != "N"):
                choice = raw_input("(Y/N)? ").upper()
            if choice == "Y":
                break
            else:
                try:
                    code = average_menu()
                except KeyboardInterrupt:
                    code = 1
    elif choice == "5":
        print
        try:
            code = csv_menu()
        except KeyboardInterrupt:
            code = 1
        while code:
            print "Quit?"
            choice = ""
            while (choice != "Y") and (choice != "N"):
                choice = raw_input("(Y/N)? ").upper()
            if choice == "Y":
                break
            else:
                try:
                    code = csv_menu()
                except KeyboardInterrupt:
                    code = 1
    elif choice == "q":
        break
        
