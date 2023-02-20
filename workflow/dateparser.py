from ast import parse
import datetime
from datetime import timedelta
import re
from dateutil.relativedelta import relativedelta

ampm_dict = {
    None: [None, None],
    "새벽": [6, "AM"],
    "아침": [9, "AM"],
    "오전": [12, "AM"],
    "점심": [1, "PM"],
    "오후": [6, "PM"],
    "저녁": [8, "PM"],
    "밤": [9, "PM"]
}

weekday_dict = {
    "": None,
    "월": 0,
    "화": 1,
    "수": 2,
    "목": 3, 
    "금": 4,
    "토": 5,
    "일": 6
}

weekday_list = ["월", "화", "수", "목", "금", "토", "일"]

day_dict = {
    "": 0,
    "오늘": 0,
    "금일": 0,
    "내일": 1,
    "익일": 1,
    "명일": 1,
    "모레": 2,
    "내일모레": 2,
    "낼모레": 2,
    "글피": 3,
    "삼명일": 3,
    "그글피": 4
}

week_dict = {
    "": 0,
    "이번주": 0,
    "담주": 1,
    "다음주": 1,
    "다담주": 2,
    "다다음주": 2
}

month_dict = {
    "": 0,
    "이달": 0,
    "이번달": 0,
    "담달": 1,
    "다음달": 1,
    "다담달": 2,
    "다다음달": 3
}

year_dict = {
    "": 0,
    "내년": 1,
    "후년": 2,
    "내후년": 3
}

abs_matchers = {
    "year": r"(\d{4})년(까지|에)?",
    "month": r"(\d+)월(까지|에)?",
    "day": r"(\d+)일(까지|에)?",
    "ampm": r"(새벽|아침|점심|오전|오후|저녁|밤)(까지|에)?",
    "hour": r"((\d+)시|\d+:\d+|정오|자정)(까지|에)?",
    "minute": r"((\d+)분|반)(까지|에)?"
}

add_matchers = {
    "year": r"(\d+)년",
    "month": r"(\d+)월",
    "week": r"(\d+)주",
    "day": r"(\d+)일",
    "hour": r"(\d+)시간",
    "minute": r"(\d+)분"
}

rel_matchers = {
    "year": r"(내년|후년|내후년)",
    "month": r"(이달|이번\s?달|담달|다음\s?달|다담달|다다음\s?달)",
    "week": r"(이번\s?주|담주|다음\s?주|다담주|다다음\s?주)",
    "day": r"(오늘|금일|내일|익일|명일|모레|내일\s?모레|낼\s?모레|글피|삼명일|그글피)"
}

def convert_dt(year, month, day, hour, minute, only_date=False, weekday=None, dt_increment=relativedelta()):
    if day < 0:
        due_dt = datetime.datetime(year, month, 1, hour, minute) + relativedelta(months=1, days=day) 
    else:
        due_dt = datetime.datetime(year, month, day, hour, minute)
    if weekday is not None:
        dt_increment += relativedelta(days=weekday) - relativedelta(days=due_dt.weekday())
    due_dt += dt_increment
    wday = due_dt.weekday()
    str_due_dt = due_dt.strftime('%m/%d/%Y') if only_date else due_dt.strftime('%m/%d/%Y %I:%M %p') 
    return str_due_dt, wday, due_dt

def parser(q):

    # split date/subject
    # [add date] + [parsed date] + [subject]
    # 주어진 자연어에 대해 가능한 모든 경우의 수를 return하도록 작성

    add_date_matcher = re.compile(r"뒤(까지)?")
    parsed_q = add_date_matcher.split(q, 1)

    if len(parsed_q) > 1:
        add_date = parsed_q[0]
        parsed_q = "".join([str(i or "") for i in parsed_q[1:]]).strip()
    else:
        add_date = ""
        parsed_q = parsed_q[0]

    parsed_date_matcher = re.compile(r"까지|에")
    parsed_subject = parsed_date_matcher.split(parsed_q, 1)
    if len(parsed_subject) > 1:
        parsed_date = parsed_subject[0]
        parsed_subject = "".join([str(i or "") for i in parsed_subject[1:]]).strip()
    else:
        parsed_date = ""
        parsed_subject = parsed_subject[0]

    due_dt = ""

    now = datetime.datetime.now()
    time_given = [False, False, False, False, False]
    inc_given = [False, False, False, False, False]
    now_dt = [now.year, now.month, now.day, now.hour, now.minute]
    abs_dt = [now.year, now.month, now.day, now.hour, now.minute]
    except_week = False

    # default: No information
    results = [{"subject": q, "due_dt": "", "allday": "", "wday": "", "str_due_dt": ""}]

    # parsed_date, add_date => datetime
    if add_date or parsed_date:
        try:
            # absolute datetime
            if parsed_date:
                due_dict = {key: None for key in abs_matchers.keys()}
                for (key, value) in abs_matchers.items():
                    matcher = re.compile(value)
                    res = matcher.search(parsed_date)
                    if res is not None:
                        due_dict[key] = res.groups()[0]
                    parsed_date = matcher.sub("", parsed_date)
                
                year = due_dict["year"]
                month = due_dict["month"]
                day = due_dict["day"]
                ampm = due_dict["ampm"]
                hour = due_dict["hour"]
                minute = due_dict["minute"]
                minute_half = due_dict["minute"]
                ampm = ampm_dict[ampm]


                if year:
                    year = int(year)
                    time_given[0] = True
                if month:
                    month = int(month)
                    time_given[1] = True
                if day:
                    day = int(day)
                    time_given[2] = True

                if isinstance(hour, str):
                    hour_q = re.compile(r"^([0-9]+):([0-9]+)$").findall(hour)
                    if hour_q:
                        hour = int(hour_q[0][0])
                        minute = int(hour_q[0][1])
                    elif hour == "정오":
                        hour = 12
                        minute = 0
                    elif hour == "자정":
                        hour = 23
                        minute = 59
                    else:
                        hour = int(re.sub(r"[^0-9]", "", hour))
                else:
                    if ampm[0]:
                        hour = ampm[0]

                if (ampm[1] == "PM") and (hour <= 12):
                    hour += 12
                    
                if minute_half == "반":
                    minute = 30
                elif isinstance(minute, str):
                    minute = int(re.sub(r"[^0-9]", "", minute))

                if isinstance(hour, int):
                    time_given[3] = True
                if isinstance(minute, int):
                    time_given[4] = True

                abs_dt = [year, month, day, hour, minute]

            # add datetime
            dt_increment = relativedelta()
            weekday = None
            if add_date:
                add_dict = {key: None for key in add_matchers.keys()}
                for (key, value) in add_matchers.items():
                    matcher = re.compile(value)
                    res = matcher.search(add_date)
                    add_dict[key] = res.groups()[0] if res is not None else ""
                    add_date = matcher.sub("", add_date)

                if add_dict["year"] != "":
                    inc_given[0] = True
                    dt_increment += relativedelta(years=int(add_dict["year"]))
                if add_dict["month"] != "":
                    inc_given[1] = True
                    dt_increment += relativedelta(months=int(add_dict["month"]))
                if add_dict["week"] != "":
                    inc_given[2] = True
                    except_week = True
                    dt_increment += relativedelta(weeks=int(add_dict["week"]))
                if add_dict["day"] != "":
                    inc_given[2] = True
                    dt_increment += relativedelta(days=int(add_dict["day"]))
                if add_dict["hour"] != "":
                    inc_given[3] = True
                    dt_increment += relativedelta(hours=int(add_dict["hour"]))
                if add_dict["minute"] != "":
                    inc_given[4] = True
                    dt_increment += relativedelta(minutes=int(add_dict["minute"]))
            
            # relative datetime
            ## add from relative date
            if parsed_date:
                rel_dict = {key: None for key in rel_matchers.keys()}
                for (key, value) in rel_matchers.items():
                    matcher = re.compile(value)
                    res = matcher.search(parsed_date)
                    rel_dict[key] = res.groups()[0] if res is not None else ""
                    parsed_date = matcher.sub("", parsed_date)

                if rel_dict["year"] != "":
                    inc_given[0] = True
                    dt_increment += relativedelta(years=year_dict[rel_dict["year"]])
                if rel_dict["month"] != "":
                    inc_given[1] = True
                    dt_increment += relativedelta(months=month_dict[rel_dict["month"].replace(" ", "")])
                if rel_dict["week"] != "":
                    inc_given[2] = True
                    dt_increment += relativedelta(weeks=week_dict[rel_dict["week"].replace(" ", "")])
                    except_week = True
                if rel_dict["day"] != "":
                    inc_given[2] = True
                    dt_increment += relativedelta(days=day_dict[rel_dict["day"].replace(" ", "")])

                ## weekday
                week_matcher = re.compile(r"([월화수목금토일](요일|욜))")
                parsed_week = week_matcher.findall(parsed_date)
                parsed_date = week_matcher.sub("", parsed_date)
                if parsed_week:
                    weekday = weekday_dict[parsed_week[0][0][0]]
                    except_week = False
                    time_given[2] = True
               
            # parsing time_given and inc_given
            # only inc_given >= time_given; first, consider inc_given, next consider time_given
            only_inc_given = [False, False, False, False, False]
            for i in range(len(inc_given)):
                if inc_given[i]:
                    if not time_given[i]:
                        only_inc_given[i] = True
                        time_given[i] = True
                    if not isinstance(abs_dt[i], int):
                        abs_dt[i] = now_dt[i]

            if sum(time_given) != 0:
                for i in range(len(time_given)):
                    if not time_given[i]:
                        abs_dt[i] = now_dt[i]
                        time_given[i] = True
                    else:
                        break
                if time_given[-1]:
                    str_due_dt, wday, due_dt = convert_dt(*abs_dt, weekday=weekday, dt_increment=dt_increment, only_date=True)
                    wday = weekday_list[wday]
                    results.append({"subject": parsed_subject,
                        "due_dt": due_dt,
                        "str_due_dt": str_due_dt,
                        "allday": "true",
                        "wday": wday})
                    str_due_dt, wday, due_dt = convert_dt(*abs_dt, weekday=weekday, dt_increment=dt_increment)
                    wday = weekday_list[wday]
                    results.append({"subject": parsed_subject, 
                        "due_dt": due_dt,
                        "str_due_dt": str_due_dt,
                        "allday": "false",
                        "wday": wday})
                    # if only_inc_given[-1]:
                    #     results[-1], results[-2] = results[-2], results[-1]
                elif time_given[-2]:
                    for minute in [59, now_dt[-1], 0]:
                        abs_dt[-1] = minute
                        str_due_dt, wday, due_dt = convert_dt(*abs_dt, weekday=weekday, dt_increment=dt_increment)
                        wday = weekday_list[wday]
                        results.append({"subject": parsed_subject,
                            "due_dt": due_dt,
                            "str_due_dt": str_due_dt,
                            "allday": "false",
                            "wday": wday})
                    if only_inc_given[-2]:
                        results[-1], results[-2] = results[-2], results[-1]
                    str_due_dt, wday, due_dt = convert_dt(*abs_dt, weekday=weekday, dt_increment=dt_increment, only_date=True)
                    wday = weekday_list[wday]
                    results.insert(1, {"subject": parsed_subject,
                        "due_dt": due_dt,
                        "str_due_dt": str_due_dt,
                        "allday": "true",
                        "wday": wday})
                elif time_given[-3]:
                    if except_week:
                        abs_dt[-1] = 0
                        abs_dt[-2] = 12
                        start_date = datetime.datetime(*abs_dt) + dt_increment
                        start_wday = start_date.weekday()
                        start_date -= relativedelta(days=start_wday)
                        for wday_i in [6, 5, 4, 3, 2, 1, 0]:
                            day_i = (start_wday + wday_i) % 7
                            abs_dt_i = start_date + relativedelta(days=day_i)
                            abs_dt[0] = abs_dt_i.year
                            abs_dt[1] = abs_dt_i.month
                            abs_dt[2] = abs_dt_i.day
                            str_due_dt, wday, due_dt = convert_dt(*abs_dt, weekday=weekday, only_date=True)
                            wday = weekday_list[wday]
                            results.append({"subject": parsed_subject,
                                "due_dt": due_dt,
                                "str_due_dt": str_due_dt,
                                "allday": "true",
                                "wday": wday})            
                    else:
                        for (hour, minute) in [(23, 59), (12, 0), (now_dt[-2], now_dt[-1])]:
                            abs_dt[-1] = minute
                            abs_dt[-2] = hour
                            str_due_dt, wday, due_dt = convert_dt(*abs_dt, weekday=weekday, dt_increment=dt_increment)
                            wday = weekday_list[wday]
                            results.append({"subject": parsed_subject,
                                "due_dt": due_dt,
                                "str_due_dt": str_due_dt,
                                "allday": "false",
                                "wday": wday})
                        str_due_dt, wday, due_dt = convert_dt(*abs_dt, weekday=weekday, dt_increment=dt_increment, only_date=True)
                        wday = weekday_list[wday]
                        results.append({"subject": parsed_subject,
                            "due_dt": due_dt,
                            "str_due_dt": str_due_dt,
                            "allday": "true",
                            "wday": wday})
                elif time_given[-4]:
                    abs_dt[-1] = now_dt[-1]
                    abs_dt[-2] = now_dt[-2]
                    for day in [-1, 1, now_dt[-3]]:
                        abs_dt[-3] = day
                        wday = weekday_list[wday]
                        results.append({"subject": parsed_subject,
                            "due_dt": due_dt,
                            "str_due_dt": str_due_dt,
                            "allday": "true",
                            "wday": wday})
                    str_due_dt, wday, due_dt = convert_dt(*abs_dt, weekday=weekday, dt_increment=dt_increment)
                    wday = weekday_list[wday]
                    results.append({"subject": parsed_subject,
                        "due_dt": due_dt,
                        "str_due_dt": str_due_dt,
                        "allday": "false",
                        "wday": wday})
                elif time_given[-5]:
                    abs_dt[-1] = now_dt[-1]
                    abs_dt[-2] = now_dt[-2]
                    for (month, day) in [(12, 31), (1, 1), (now_dt[1], now_dt[2])]:
                        abs_dt[1] = month
                        abs_dt[2] = day
                        str_due_dt, wday, due_dt = convert_dt(*abs_dt, weekday=weekday, dt_increment=dt_increment, only_date=True)
                        wday = weekday_list[wday]
                        results.append({"subject": parsed_subject,
                            "due_dt": due_dt,
                            "str_due_dt": str_due_dt,
                            "allday": "true",
                            "wday": wday})
                    str_due_dt, wday, due_dt = convert_dt(*abs_dt, weekday=weekday, dt_increment=dt_increment)
                    wday = weekday_list[wday]
                    results.append({"subject": parsed_subject,
                        "due_dt": due_dt,
                        "str_due_dt": str_due_dt,
                        "allday": "false",
                        "wday": wday})

        except Exception as e:
            return results[::-1]
        
    return results[::-1]
