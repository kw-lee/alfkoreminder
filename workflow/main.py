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

def main(wf):
    args = wf.args[0]
    
    # parse input
    results = parser(args)

    for item in results:
        subject = item["subject"]
        due_dt = item["due_dt"]
        allday = item["allday"]
        wday = item["wday"]
        if allday == "true":
            subtitle = f"{due_dt} ({wday}) 하루 종일"
        elif allday == "false":
            due_d, due_t = due_dt.split(" ", 1)
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
    # print(parser("다음주 목요일 오후 6시까지 청소하기"))
