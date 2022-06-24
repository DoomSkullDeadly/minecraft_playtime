from datetime import datetime as dt
from datetime import timedelta
import os
import gzip


mc_dir = r'C:\Users\\'+os.environ.get('USERNAME')+r'\\AppData\Roaming\.minecraft'  # change if different i guess lol


def get_playtime(log_dir: str):  # gets the playtime from a log file
    log_dir = mc_dir + r'\\logs\\' + log_dir

    if '.gz' in log_dir:  # opens zipped log file with gzip
        with gzip.open(log_dir, 'rb') as f:
            ff = f.readlines()
    else:
        with open(log_dir, 'r') as f:  # opens log file if not zip
            ff = f.readlines()

    if '.gz' in log_dir:
        s = ff[0][1:9].decode('utf-8')
    else:
        s = ff[0][1:9]

    if not s.isalnum():  # checks for log time format, isalnum if forge? NOT VANILLA
        if '.gz' in log_dir:
            start_time = dt.strptime(ff[0][1:9].decode('utf-8'), '%H:%M:%S')  # start time of log
        else:
            start_time = dt.strptime(ff[0][1:9], '%H:%M:%S')
        prev_time = start_time

        for line in ff[1:]:
            if len(line) < 10 or (line[0] != '[' and line[9] != ']'):
                continue
            if '.gz' in log_dir:
                time = line[1:9].decode('utf-8')
            else:
                time = line[1:9]
            current_time = dt.strptime(time, '%H:%M:%S')  # the current time in log line for comparison
            if prev_time > current_time:  # adds a day to datetime if time goes past midnight, for delta calc
                current_time += timedelta(hours=24)
            prev_time = current_time

        time_delta = prev_time - start_time

    else:
        if '.gz' in log_dir:
            start_time = dt.strptime(ff[0][1:22].decode('utf-8')+'000', '%d%b%Y %H:%M:%S.%f')
            end_time = dt.strptime(ff[-1][1:22].decode('utf-8')+'000', '%d%b%Y %H:%M:%S.%f')
            time_delta = end_time - start_time
        else:
            start_time = dt.strptime(ff[0][1:22]+'000', '%d%b%Y %H:%M:%S.%f')
            end_time = dt.strptime(ff[-1][1:22]+'000', '%d%b%Y %H:%M:%S.%f')
            time_delta = end_time - start_time

    return time_delta


if __name__ == '__main__':  # TODO: Support for multiple mc directories
    logs = os.listdir(mc_dir+r'\logs')  # gets all files in logs folder
    to_remove = []
    for log in logs:  # collect files that need to be removed
        if 'debug' in log:
            to_remove.append(log)
    for i in to_remove:  # remove unneeded files
        logs.remove(i)

    playtimes = []
    for log in logs:  # iter through logs
        try:
            playtimes.append(get_playtime(log))
        except:
            print(f"Something went wrong with {log}")

    total = 0
    for time in playtimes:
        total += time.total_seconds()

    print(timedelta(seconds=total))
    hours = total // 3600
    total -= (hours * 3600)
    minutes = total // 60
    seconds = total - (minutes * 60)
    print('{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds)))
    input(print("[Enter] to confirm"))
