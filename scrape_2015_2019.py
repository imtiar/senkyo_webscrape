#2015年と、2019年の選挙結果を外部結合させている
#結合の目的は、各立候補者ごとの、2015、2019年それぞれにおける選挙結果をみやすくすることである
#最終的に、[氏名、2015の選挙結果、2019の選挙結果、~以降両年の細かいデータとなっている(scrape_2015,2019の各要素)]
#両年の選挙結果は、当選→○, 落選→×, 出馬せず→None としている

import pandas as pd

df_1 = pd.read_csv('senkyo_2015.csv')
df_2 = pd.read_csv('senkyo_2019.csv')

df = pd.merge(df_1, df_2, on=['氏名', '都道府県', '選挙区'], how='outer')


col = df.columns.tolist()

col.remove('氏名')
col.insert(0, '氏名')

df = df[col]

df.insert(3, '2015の状況', 0)
df.insert(4, '2019の状況', 0)

for i in range(len(df['当選の有無_x'])):
  if df['当選の有無_x'][i] == '当':
    df['2015の状況'][i] = 'win'
  elif df['当選の有無_x'][i] == '落':
    df['2015の状況'][i] = 'lose'
  else:
    df['2015の状況'][i] = None
    
for i in range(len(df['当選の有無_y'])):
  if df['当選の有無_y'][i] == '当':
    df['2019の状況'][i] = 'win'
  elif df['当選の有無_y'][i] == '落':
    df['2019の状況'][i] = 'lose'
  else:
    df['2019の状況'][i] = None

df.to_csv('senkyo_2015_2019.csv')
   
