import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

#まずヘッダーを作り、都道府県ごと、そしてその都道府県の中の選挙区ごとに各要素を抜き出している

HEADER = ['都道府県', '選挙区', '当選の有無', '得票数', '得票率', '氏名', '年齢', '党派', '新旧', '当選回数', '代表的肩書']

index = 0

with open('senkyo_2019.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(HEADER)

    for i in range(46):
      index += 1

# indexが3, 4, 7, 8, 13の時は不適なURLなため
      if index in [3, 4, 7, 8, 13]:
        continue
       
      load_url = f"https://www.yomiuri.co.jp/election/local/2019/yh_YH{index:02}XXXXXX000"
      html = requests.get(load_url)

      soup = BeautifulSoup(html.content, "html.parser")
      senkyos = soup.find_all("section", class_ = "election-local-2019-brief-section election-local-2019-yh")

      pref = soup.find("div", class_="election-local-2019-common-electoral-nav__title").text

      for senkyo in senkyos:
      
        senkyoku = senkyo.find('h2', class_ = "election-local-2019-common-section__title").text
        vote_num = senkyo.find_all('span', class_="number")
        vote_per = senkyo.find_all('span', class_="percent")
        name = senkyo.find_all('div', class_="election-local-2019-brief-section-person__name")
        age = senkyo.find_all('div', class_="election-local-2019-brief-section-person__age")
        party = senkyo.find_all('div', class_="election-local-2019-brief-section-person__party")
        oldnew = senkyo.find_all('div', class_="election-local-2019-brief-section-person__oldnew")
        number = senkyo.find_all('div', class_="election-local-2019-brief-section-person__number-of-elected")
        pr_title = senkyo.find_all('div', class_="election-local-2019-brief-section-person__career")

        length = len(name)

 # 各行に、"result--tosen"というclassが付いていれば当選、ということだったので、選挙区ごとにリストを作り、当選をした人のインデックスには1をたて、落選者のところには0を立てた

        if vote_num != []:
            length_tosen = len(senkyo.find_all('li', class_ = "result--tosen"))
            toraku = [1] * length_tosen + [0] * (length-length_tosen)
 # 無投票（立候補者数 < 選挙ポスト数)のとき全てを1にしている
        else:
            toraku = [1] * length

        for i in range(len(name)):
          tor = "当" if toraku[i] == 1 else "落"
          vot_num = "無投票" if vote_num == [] else int(vote_num[i].text.replace(",", ""))
          vot_per = "無投票" if vote_per == [] else float(vote_per[i].text.replace("%", ""))
          nam = name[i].span.text
          ag = int(age[i].span.text)
          par = party[i].span.text
          ol = oldnew[i].span.text
          num = int(number[i].span.text) if tor == "当" else None
          pr = pr_title[i].span.text

          row = [pref, senkyoku, tor, vot_num, vot_per, nam, ag, par, ol, num, pr]
          writer.writerow(row)

df = pd.read_csv('senkyo_2019.csv')
print(df)








