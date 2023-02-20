# alfkoreminder : Korean Reminder Workflow for Alfred

## 설치하기

- [releases](../../releases/latest) 페이지의 `koreminder.alfredworkflow`를 다운로드 받아서 실행하면 됩니다.

### 참고

워크플로우의 실행을 위해서는 python3와 다음의 패키지가 필요합니다.

* [python-dateutil](https://dateutil.readthedocs.io/en/stable/)
* [requests](https://requests.readthedocs.io/en/latest/)

다음의 명령어로 필요한 패키지들을 설치할 수 있습니다.

```bash
/usr/bin/pip3 install python-dateutil requests
```

## 사용법

기본적으로는 `[~뒤(까지)] [~에/까지] ~하기`와 같이 사용합니다. `[]` 안의 내용은 생략할 수 있으나 **순서는 바꿀 수 없습니다!**

```
rk 내일 새벽 1시까지 부장님께 이메일 보내기
rk 3주 뒤 월요일 오후 3시까지 작업하기
rk 2022년 12월 31일 밤 11시 59분에 커밋하기
rk 오늘안에 퇴사하기
```

![`rk 내일 새벽 1시까지 부장님께 이메일 보내기`](assets/ex1.png)
![`rk 3주 뒤 월요일 오후 3시까지 작업하기`](assets/ex2.png)
![`rk 2022년 12월 31일 밤 11시 59분에 커밋하기`](assets/ex3.png)
![`rk 오늘안에 퇴사하기`](assets/ex4.png)

와 같은 식으로 사용할 수 있습니다.

## 날짜 부분에 올 수 있는 말

* 연: ㅇㅇㅇㅇ년, 내년, 후년, 내후년
* 월: ㅇㅇ월, 이달, 이번달, 담달, 다음달, 다담달, 다다음달
* 주: 이번주, 담주, 다음주, 다담주, 다다음주
* 일: 오늘, 금일, 내일, 익일, 명일, 모레, 내일모레, 낼모레, 글피, 삼명일, 그글피
* 요일: 월, 화, 수, 목, 금, 토, 일
* 시각: 새벽, 아침, 오전, 점심, 오후, 저녁, 밤, ㅇㅇ시, ㅇㅇ분, 반, ㅇㅇ:ㅇㅇ

## 참고 자료

* https://github.com/mollax/fanatstical_korean_alfred_workflow
* https://www.alfredforum.com/topic/15992-applescript-reads-alfred-environment-variables-in-wrong-encoding/

## 버전 정보

* v0.0.3: 날짜 표시 관련 버그 수정
* v0.0.2: 버그 수정, `ㅇㅇ분 뒤 할 일`의 순서 수정
* v0.0.1: 워크플로우 작성