import csv
from datetime import datetime

file_path = "/Users/denis/root/bohdan/input/binance_m1_usdt_btc.csv"


def get_frame(input_path, minutes, output_dir):
    last_index = input_path.rfind('/')
    file_name = input_path[last_index:]
    output_file_name = file_name.replace('1', str(minutes))
    with open(input_path, "r") as from_file, open(output_dir + output_file_name, "w") as to_file:
        lines = csv.reader(from_file)
        next(lines, None)
        count = 0
        start_time = 0
        for r in lines:
            if str(r).startswith("2017-12-18 10:00"):
                a = 0
            count += 1
            if start_time == 0:
                open_time = r[0]
                open_value = r[1]
                high_value = float(r[2])
                low_value = float(r[3])
                volume = float(r[5])
                quote_volume = float(r[6])
            elif count < minutes:
                high_value = high_value if high_value > float(r[2]) else float(r[2])
                low_value = low_value if low_value < float(r[3]) else float(r[3])
                volume += float(r[5])
                quote_volume += float(r[6])
            elif count == minutes:
                close = r[4]
                result = [open_time, open_value, str(high_value), str(low_value), close, str(volume), str(quote_volume)]
                res = "[" + ", ".join(result) + "]"
                to_file.write(res + "\n")
                count = 0


get_frame(file_path, 60, "/Users/denis/root/bohdan/output")
