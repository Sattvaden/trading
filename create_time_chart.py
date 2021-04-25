import csv
from datetime import datetime, timedelta
from sys import argv

DATE_PATTERN = "%Y-%m-%d %H:%M:%S%z"


def get_time(str_value):
    return datetime.strptime(str_value, DATE_PATTERN)


def parse_to_string(dt_obj):
    return dt_obj.strftime(DATE_PATTERN)


def get_data(input_file):
    date, open_, high, low, close, volume, quote_volume = [], [], [], [], [], [], []
    with open(input_file, "r") as from_file:
        lines = csv.reader(from_file)
        next(lines, None)
        for r in lines:
            date.append(get_time(r[0]))
            open_.append(float(r[1]))
            high.append(float(r[2]))
            low.append(float(r[3]))
            close.append(float(r[4]))
            volume.append(float(r[5]))
            quote_volume.append(float(r[6]))
    return [date, open_, high, low, close, volume, quote_volume]


def merge(current_line, line_to_add):
    current_line[2] = max(current_line[2], line_to_add[2])
    current_line[3] = min(current_line[2], line_to_add[3])
    current_line[4] = line_to_add[4]
    current_line[5] = round(current_line[5] + line_to_add[5], 8)
    current_line[6] = round(current_line[6] + line_to_add[6], 6)
    return current_line


def add_to_result(result, row):
    temp = [parse_to_string(row[0])]
    for i in range(1, len(row)):
        temp.append(str(row[i]))
    result.append(",".join(temp))


def fill_gap_if_necessary(result, row, frame):
    if not result:
        return result
    last_row = result[-1].split(',')
    last_row[5], last_row[6] = '0', '0'
    last_time = get_time(last_row[0])
    last_time += timedelta(minutes=frame)
    while last_time < row[0]:
        last_row[0] = parse_to_string(last_time)
        result.append(",".join(last_row))
        last_time += timedelta(minutes=frame)
    return result


def within_delta(current_time, open_time, delta):
    return current_time - open_time < delta


def round_time(dt_obj, frame):
    m = dt_obj.minute - dt_obj.minute % frame
    return dt_obj.replace(minute=m)


def get_frame(input_file, frame):
    res = []
    data = get_data(input_file)
    row = [round_time(data[0][0], frame), data[1][0], data[2][0], data[3][0], data[4][0], data[5][0], data[6][0]]
    delta = timedelta(minutes=int(frame))
    for i in range(1, len(data[0])):
        row_i = [data[0][i], data[1][i], data[2][i], data[3][i], data[4][i], data[5][i], data[6][i]]
        if within_delta(data[0][i], row[0], delta):
            merge(row, row_i)
        else:
            add_to_result(fill_gap_if_necessary(res, row, frame), row)
            row_i[0] = round_time(data[0][i], frame)
            row = row_i
    return res


def write_to_file(result, to_file):
    with open(to_file, "w") as to_file:
        for i in range(0, len(result)):
            to_file.write(result[i] + "\n")


if len(argv) != 4:
    print("wrong number of arguments")
    exit()
start = datetime.now()
write_to_file(get_frame(input_file=argv[1], frame=int(argv[3])), to_file=argv[2])
print(datetime.now() - start)
