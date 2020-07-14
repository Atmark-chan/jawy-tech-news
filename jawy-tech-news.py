  ##### import #####

import pywikibot as pwb
import re
import datetime

############################################################

  ##### 準備 #####

m = 'meta'
i = 'incubator'
usr = 'Atmark-chan-Bot'
meta = pwb.Site(m, m, usr)
incub = pwb.Site(i, i, usr)

############################################################

  ##### 日付等取得 #####

# 今日
tdy = datetime.date.today()
# 曜日
wd = tdy.weekday()
# 直前の月曜日（今日を除く）
if wd == 0:
  mon = tdy + datetime.timedelta(days = -7)
else:
  mon = tdy + datetime.timedelta(days = -wd)
# ISO
iso = mon.isocalendar()
# 年
y = iso[0]
# 週
w = iso[1]

  ##### 配信元ページ取得～文字列生成 #####

mPageN = f'Tech/News/{y}/{w}/ja'
mPage = pwb.Page(meta, mPageN)
txt = mPage.text
id = mPage.latest_revision_id
m = re.search(r'<section begin="[^"]*"\/>[\s\S]*<section end="[^"]*"\/>', txt)
mainTxt = m.group()

addTxt \
  = '\n\n' \
   f'== [[m:Special:MyLanguage/Tech/News/{y}/{w}|Tech News: {y}-{w}]] ==' \
    '\n\n' \
   f'{mainTxt}' \
    '\n\n' \
   '----' \
    '\n' \
   f'[[m:{mPageN}]]<span style="font-size:smaller;">（[[m:Special:Permalink/{id}|固定]]）</span>より。--~~~~'

############################################################

  ##### 配信先ページ取得～編集 #####

iPage = pwb.Page(incub, 'Wy/ja/Wikivoyage:お知らせ')
iPage.text += addTxt
summ = f'/* Tech News: {y}-{w} */ [[m:Special:MyLanguage/Tech/News|Tech News]] 配信。[[m:{mPageN}]]（[[m:Special:Permalink/{id}|固定]]）より'
iPage.save(summary = summ, minor = False)