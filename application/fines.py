import datetime

fine_ranges = [[0,10],[11,15],[16,20],[21,25],[26,31],[31,35],[36,40],[41,45]]
fines = [30, 80, 120, 170, 230, 300, 400, 510, 630]

speed_limit = 80
exit_threshold_mins = 4
t_distance = 2690

# file reading
filePath = "data/tdata-csv.csv"

reg_time = []
errors = []

try:
    file_read = open(filePath, "r")
except:
    raise FileNotFoundError("File couldn't be opened")

if filePath.endswith("txt"):
    for line in file_read.readlines():
        line_data = line.split()
        if len(line_data[0]) <= 6 and line_data[0].isalnum() == True:
            reg_time.append(line_data)  
        else:
            line_data.pop(1)
            line_data.append("Invalid License Plate")
            errors.append(line_data)      
elif filePath.endswith("csv"):
    for line in file_read.readlines():
        line_data = line.split(",")
        if len(line_data[0]) < 7 and line_data[0].isalnum() == True:
            reg_time.append(line_data)
        else:
            line_data.pop(1)
            line_data.append("Invalid License Plate")
            errors.append(line_data)  
    for i, item in enumerate(reg_time):
        item[1] = item[1].strip("\n") # strip the newline register of the end of the string
else:
    raise errors("Incompatible File Type")

# helper functions
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

def CalculateDuration(timeIn, timeOut) -> datetime.time:
    min_date = datetime.date.min
    return datetime.datetime.combine(min_date, timeOut) - datetime.datetime.combine(min_date, timeIn)

def CalculateAvgSpeed(duration_mins):
    return (t_distance / 1000) / (duration_mins / 60)

# fines are calculated by reversing through the fine range list until the speed is met
def CalculateFines(speed):
    over = speed - speed_limit
    if over == 0:
        return None
    elif over > fine_ranges[len(fine_ranges)-1][0]:
        return fines[len(fines)-1]    # return the last fine in the list
    else:
        for i, x in reversed(list(enumerate(fine_ranges))):
            if over >= fine_ranges[i][0]:
                return fines[i]
                break

def GenerateFines(rtimes_list_in):
    rds_list_out = rtimes_list_in   # reg, duration, speed
    for i, item in enumerate(rds_list_out):
        duration = CalculateDuration(StrToTime(item[1]), StrToTime(item[2]))
        speed = CalculateAvgSpeed(TimeToIntMins(duration))
        fine = CalculateFines(speed)

        item.append(str(duration))
        item.append(speed)
        item.append(fine)

        if speed < 0:
            errors.append(item)
            errors[len(errors)-1].append("Vehicle did not exit")
        elif TimeToIntMins(duration) >= exit_threshold_mins:
            errors.append(item)
            errors[len(errors)-1].append("Vehicle did not leave after {} minute exit threshold!".format(exit_threshold_mins))
        
    return rds_list_out


a = GenerateFines(RemoveDuplicates(FindTimeInOut(reg_time)))

write_file = open("data/out/fines_out.txt", "w")
error_write_file = open("data/out/errors_out.txt", "w")

for i, item in enumerate(a):
    if len(item) > 2:
        output_string = "{}.  {}\t {}\t {}\t {}\t {:.2f}km/h\t {}\n".format(i,item[0], item[1], item[2], item[3], item[4], item[5])
    else:
        output_string = "{}.  {}\t {}\t {}\t {}\t {:.2f}km/h\t ${}\n".format(i,item[0], item[1], item[2], item[3], item[4], item[5])
    print(output_string.strip("\n"))
    write_file.write(output_string)

for i,item in enumerate(errors):
    if len(item) <= 2:
        output_string = "Err {}.  {}\t {}\n".format(i, item[0], item[1])
    else:
         output_string = "Err {}.  {}\t {}\t {}\t {}\t {:.2f}km/h\t {}\t {}\n".format(i, item[0], item[1], item[2], item[3], item[4], item[5], item[6])

    print(output_string.strip("\n"))
    error_write_file.write(output_string)