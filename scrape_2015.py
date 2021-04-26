#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr  4 00:16:34 2021

@author: imtiar
"""

import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd

#まずヘッダーを作り、都道府県ごと、そしてその都道府県の中の選挙区ごとに各要素を抜き出している

# 行をまず作成
HEADER = ['都道府県', '選挙区', '当選の有無', '得票数', '得票率', '氏名', '年齢', '党派', '新旧', '当選回数', '代表的肩書']

# 変数を作っている (URLの末尾が変わるため)
index = 0

with open('senkyo_2015.csv', 'w', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(HEADER)

    for i in range(46):
      index += 1

# indexが3, 4, 7, 8, 13の時はURLが存在しないため
      if index in [3, 4, 7, 8, 13]:
        continue
        
#urlの中身を適宜変えている
      load_url = f"https://www.yomiuri.co.jp/election/local/2015/kaihyou/yh{index:02}.html"
      html = requests.get(load_url)

      soup = BeautifulSoup(html.content, "html.parser")
      
      senkyos = soup.find_all(class_= "cndt")

      prefecture = soup.find('div', class_="loc-place").h3.text

      for senkyo in senkyos:
              senkyoku = senkyo.find('a').text
              toraku = senkyo.find_all('td', class_="toraku")
              vote = senkyo.find_all('td', class_="vote")
              name = senkyo.find_all('td', class_="name")
              age = senkyo.find_all('td', class_="age")
              party = senkyo.find_all('td', class_="party")
              oldnew = senkyo.find_all('td', class_="oldnew")
              number = senkyo.find_all('td', class_="number")
              pr_title = senkyo.find_all('td', class_="pr-title")
            
# 上のは選挙区ごとに見ていて、下の場所は選挙区の中をみている
# .textの意味は、タグの中にある物の中で、textのみを拾ってきてくれる(つけとかないとタグもつけてくる)
# 数字の部分はhtmlの状態では文字なので、intをつけることで、数字に変換している。
              for i in range(len(toraku)):
                tor = "当" if toraku[i].text == "当選" else "落"
                vot = "無投票" if vote == [] else int(vote[i].contents[0].replace(",", ""))
                vot_per = "無投票" if vote == [] else float(vote[i].contents[1].text.replace("(", "").replace(")", "").replace("%", ""))
                nam = name[i].text
                ag = int(age[i].text)
                par = party[i].text
                ol = oldnew[i].text
                num = int(number[i].text) if tor == "当" else None
                pr = pr_title[i].text
 
 # rowでfor文で回したものを入れて、writerowでfor文ごとに入れている
                row = [prefecture, senkyoku, tor, vot, vot_per, nam, ag, par, ol, num, pr]
                writer.writerow(row)
 # ここから下は確認のために出力
df = pd.read_csv('senkyo_2015.csv')
print(df)

