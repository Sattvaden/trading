import csv
from datetime import datetime, timedelta

file_path = "/Users/denis/root/bohdan/input/binance_m1_usdt_btc.csv"


def get_frame(input_path, frame, output_dir):
    last_index = input_path.rfind('/')
    file_name = input_path[last_index:]
    output_file_name = file_name.replace('1', str(frame))
    frame_delta = timedelta(minutes=frame - 1)
    with open(input_path, "r") as from_file, open(output_dir + output_file_name, "w") as to_file:
        lines = csv.reader(from_file)
        next(lines, None)
        start = True
        for r in lines:
            if start:
                open_time = datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S%z")
                open_value = r[1]
                high_value = float(r[2])
                low_value = float(r[3])
                volume = float(r[5])
                quote_volume = float(r[6])
                start = False
                continue
            r_time = datetime.strptime(r[0], "%Y-%m-%d %H:%M:%S%z")
            delta = r_time - open_time
            if delta < frame_delta:
                high_value = high_value if high_value > float(r[2]) else float(r[2])
                low_value = low_value if low_value < float(r[3]) else float(r[3])
                volume += float(r[5])
                quote_volume += float(r[6])
            elif delta == frame_delta:
                close = r[4]
                result = [open_time.strftime("%Y-%m-%d %H:%M:%S%z"),
                          open_value, str(high_value),
                          str(low_value),
                          str(close),
                          str(volume),
                          str(round(quote_volume, 6))]
                res = "[" + ", ".join(result) + "]"
                to_file.write(res + "\n")
                start = True


get_frame(file_path, 5, "/Users/denis/root/bohdan/output")
