import pandas as pd
from datetime import datetime
import pytz
import sys
from colorama import Fore, init
import os
import time
init()

begin = 95

day_of_week_dict = {0: '一', 1: '二', 2: '三', 3: '四', 4: '五', 5: '六', 6: '日'}

def add_zero(clock):
    ret = str(clock)
    # if len(ret) == 1: return '0' + ret
    return ret

def get_strptime(time):
  return datetime.strptime(time, '%Y-%m-%d %H:%M:%S')

def get_cur_time():
  return str(datetime.now(pytz.timezone('America/Los_Angeles')))[0:19]

def get_time_from_now(time):
  return get_strptime(time) - get_strptime(get_cur_time())

def get_day_of_week(date_string):
  return '(' + day_of_week_dict[datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S').weekday()] + ')'

def parse_diff(diff):
  delimeter = ' '
  days = diff.days
  hours = diff.seconds // 3600
  minutes = (diff.seconds % 3600) // 60
  seconds = diff.seconds % 60
  time_list = [days, hours, minutes, seconds]
  str_list = [''] * 4
  frame_list = ["day", "hour", "minute", "second"]
  for i in range(4):
    cur_num = time_list[i]
    if cur_num == 0:
      continue
    cur_time_str = str(cur_num) + " " + frame_list[i]
    str_list[i] = cur_time_str
    if cur_num > 1:
      str_list[i] += 's'
    if i > 0 and str_list[i - 1] != '' and str_list[i - 1] != delimeter:
      str_list[i] = delimeter + str_list[i]
  return ''.join(str_list)

def clear_screen():
  os.system('cls')
  # print('\033[H')

def time_conversion(time):
    date = time[5:11]
    clock = int(time[11:13])
    
    if clock == 0:
        return date + "12 am"
    elif clock == 12:
        return date + add_zero(clock) + time[13:len(time) - 3] + " pm"
    elif clock < 12:
        return date + add_zero(clock) + time[13:len(time) - 3] + " am"
    else:
        return date + add_zero(clock - 12) + time[13:len(time) - 3] + " pm"

def print_game(time, day_of_week, game, diff_str):
    if "Warriors" in game:
        print(Fore.RESET + time, day_of_week + Fore.BLUE + " " + game + Fore.RESET + diff_str)
    elif "Kings" in game:
        print(Fore.RESET + time, day_of_week + Fore.MAGENTA + " " + game + Fore.RESET + diff_str)
    else:
        print(Fore.RESET + time, day_of_week + " " + game + diff_str)

def next_n_games_dynamic(n):
  df = pd.read_csv("Sport Schedule.csv")
  cur_time = get_cur_time()
  for i in range(begin, len(df)):
    row = df.loc[i]
    if row['Time'] < cur_time: continue
    while True:
      print(f"As of {get_cur_time()}")
      for j in range(i, i + n):
          if j >= len(df): return
          game_time = df.loc[j]['Time']
          diff = get_time_from_now(game_time)
          diff_str = " (" + parse_diff(diff) + ")"
          day_of_week = get_day_of_week(game_time)
          print_game(time_conversion(game_time), day_of_week, df.loc[j]['Game'], diff_str)
      time.sleep(1)
      clear_screen()

def next_n_games(n = 10, dynamic = False):
  if dynamic: next_n_games_dynamic(n)
  df = pd.read_csv("Sport Schedule.csv")
  cur_time = get_cur_time()
  for i in range(begin, len(df)):
    row = df.loc[i]
    if row['Time'] < cur_time: continue
    print(f"As of {cur_time}")
    for j in range(i, i + n):
        if j >= len(df): return
        game_time = df.loc[j]['Time']
        diff = get_time_from_now(game_time)
        diff_str = " (" + parse_diff(diff) + ")"
        day_of_week = get_day_of_week(game_time)
        print_game(time_conversion(game_time), day_of_week, df.loc[j]['Game'], diff_str)
    return

size = len(sys.argv)
if size == 3:
  next_n_games(int(sys.argv[1]), sys.argv[2] == 'dynamic')
elif size == 2:
  next_n_games(int(sys.argv[1]))
else:
  next_n_games()
