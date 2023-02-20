"""
Korea Reminder Workflow for Alfred 5
Copyright (c) 2022 Kyeongwon Lee

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
from workflow import Workflow3
from dateparser import parser
from subprocess import Popen, PIPE
import os

def addReminder():
    subject = os.environ['subject'].replace('"', '\\"')
    due_year = os.environ['due_year']
    due_month = os.environ['due_month']
    due_day = os.environ['due_day']
    due_hour = os.environ['due_hour']
    due_minute = os.environ['due_minute']
    str_due_dt = os.environ['str_due_dt']
    allday = os.environ['allday']
    script = f'''
set todo to "{subject}" as string
set due_dt to (current date)
set str_due_dt to "{str_due_dt}"
set year of due_dt to "{due_year}"
set month of due_dt to "{due_month}"
set day of due_dt to "{due_day}"
set hours of due_dt to "{due_hour}"
set minutes of due_dt to "{due_minute}"
set allday to "{allday}" as string
tell application "Reminders"
    activate
    if str_due_dt is not equal to "" then
    if allday is equal to "true" then
        make new reminder at end with properties {{name:todo, allday due date:due_dt}}
    else
        make new reminder at end with properties {{name:todo, due date:due_dt}}
    end if
    else
    make new reminder at end with properties {{name:todo}}
    end if
end tell
    '''
    args = []
    p = Popen(['/usr/bin/osascript', '-'] + args,
              stdin=PIPE, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate(script.encode("utf-8"))
    print(stdout + stderr)

def main(wf):
    args = wf.args[0]
    
    # parse input
    results = parser(args)

    for item in results:
        subject = item["subject"]
        str_due_dt = item["str_due_dt"]
        allday = item["allday"]
        wday = item["wday"]
        item['due_year'] = str(item['due_dt'].year) if item['due_dt'] else ''
        item['due_month'] = str(item['due_dt'].month) if item['due_dt'] else ''
        item['due_day'] = str(item['due_dt'].day) if item['due_dt'] else ''
        item['due_hour'] = str(item['due_dt'].hour) if item['due_dt'] else ''
        item['due_minute'] = str(item['due_dt'].minute) if item['due_dt'] else ''
        item['due_dt'] = None
        if allday == "true":
            subtitle = f"{str_due_dt} ({wday}) 하루 종일"
        elif allday == "false":
            due_d, due_t = str_due_dt.split(" ", 1)
            subtitle = f"{due_d} ({wday}) {due_t}"
        else:
            subtitle = ""
        wf.add_item(
            title=f"미리알림에 \'{subject}\' 일정 추가",
            subtitle=subtitle,
            autocomplete=subject,
            arg=subject,
            copytext=subject,
            largetext=subject,
            variables=item,
            valid=True
        )

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
    # print(parser("다음주 목요일까지 청소하기"))
