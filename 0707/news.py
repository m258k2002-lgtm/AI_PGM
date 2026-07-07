from datetime import datetime

# 경기 결과 입력 받는 곳
place=input("경기가 열린 곳은? ")
time=input("경기가 열린 시간은? ")
opponent=input("상대 팀은? ")
goals=input("손흥민은 몇 골을 넣었나요? ")
aids=input("도움은 몇 개인가요? ")
score_me=input("손흥민 팀이 넣은 골 수는? ")
score_you=input("상대 팀이 넣은 골 수는? ")

# 기사 작성하는 곳
news="[프리미어 리그 속보("+str(datetime.now())+")]\n"
news=news+"손흥민 선수는 "+place+"에서 "+time+"에 열린 경기에 출전하였습니다. "
news=news+"상대 팀은 "+opponent+"입니다. "

if score_me>score_you:
    news=news+"손흥민 선수의 팀이 "+score_me+"골을 넣어 "+score_you+"골을 넣은 상대 팀을 이겼습니다. "
elif score_me<score_you:
    news=news+"손흥민 선수의 팀이 "+score_me+"골을 넣어 "+score_you+"골을 넣은 상대 팀에게 졌습니다. "
else:
    news=news+"두 팀은 "+score_me+"대"+score_you+"로 비겼습니다. "

if int(goals)>0 and int(aids)>0:
    news=news+"손흥민 선수는 "+goals+"골에 도움 "+aids+"개로 승리를 크게 이끌었습니다. "
elif int(goals)>0 and int(aids)==0:
    news=news+"손흥민 선수는 "+goals+"골로 승리를 이끌었습니다. "
elif int(goals)==0 and int(aids)>0:
    news=news+"손흥민 선수는 골은 없지만 도움 "+aids+"개로 승리하는 데 공헌하였습니다. "
else:
    news=news+"아쉽게도 이번 경기에서 손홍민의 발끝은 침묵을 지켰습니다. "

print(news)

# 음성으로 들려주는 곳
import asyncio 
import edge_tts
import os

text = news
voice = "ko-KR-SunHiNeural" 
output_file = "news_edge.mp3"
# 2. 음성 생성 및 저장 함수
async def main():
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)

# 3. 실행 및 윈도우 기본 플레이어로 재생
asyncio.run(main())
os.system("start " + output_file)