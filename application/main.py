import datetime

fines = [0, 30, 80, 120, 170, 230, 300, 400, 510, 630]

speedLimit = 80

# file reading
filePath = "data/tdata-csv.csv"

reg_time = []

file_read = open(filePath, "r")
if filePath.endswith("txt"):
    for line in file_read.readlines():
        line_data = line.split()
        reg_time.append(line_data)
elif filePath.endswith("csv"):
    for line in file_read.readlines():
        line_data = line.split(",")
        reg_time.append(line_data)
    for i, item in enumerate(reg_time):
        item[1] = item[1][:-1] # strip the newline register of the end of the string
else:
    raise TypeError("Incompatible File Type")

# helper functions
def CalculateDuration(timeIn, timeOut):
    return datetime.datetime.combine(datetime.date.today(), timeOut) - datetime.datetime.combine(datetime.date.today(), timeIn)

def StrToTime(time):
    return datetime.datetime.strptime(time, "%H:%M:%S").time()

def TimeToIntMins(time):
    total_seconds = int(time.total_seconds())
    return total_seconds/60

def FindTimeInOut(reg_list):
    new_reg_list = []
    for i, reg in enumerate(reg_list):
        plate = reg[0]
        timeIn = reg[1]
        for x in range(i+1, len(reg_list)):
            if reg_list[x][0] in plate:
                timeOut = reg_list[x][1]
                break
            else:
                timeOut = "00:00:00"
        new_reg_list.append([plate, timeIn, timeOut])
    
    return new_reg_list

def RemoveDuplicates(list):
    new_list = list
    
    for i, item in enumerate(new_list):
        for x in range(i+1, len(new_list)):
            if new_list[x][0] in item[0]:
                new_list.pop(x)
                break
    
    return new_list

def CalculateAvgSpeed(duration_mins, distance_mtrs):
    return (distance_mtrs / 1000) / (duration_mins / 60)

def CalculateFines(speed):
    over = speed - speedLimit
    if over > 45:
        return fines[9]
    if over > 10 and over < 45:
        return fines[round(over/5)]
    
g = RemoveDuplicates(FindTimeInOut(reg_time))

t_distance = 2690

for i, item in enumerate(g):
    speed = CalculateAvgSpeed(TimeToIntMins(CalculateDuration(StrToTime(item[1]), StrToTime(item[2]))), t_distance)
    fine = CalculateFines(speed)
    if speed < 0:
        print(item[0],"did not exit")
    else:
        # plate, in, out, duration, speed
        print("{}\t{}\t{}\t{}\t  {:.2f}km/h\t{}".format(item[0], item[1], item[2], CalculateDuration(StrToTime(item[1]), StrToTime(item[2])), speed, fine))
