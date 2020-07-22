  ##### import #####

import pywikibot as pwb
import re
import datetime

############################################################

  ##### 準備 #####

m = 'meta'
i = 'incubator'
usr = 'Atmark-chan-Bot'
meta = pwb.Site(m, m, usr) # Atmark-chan-Bot として Meta へ
incub = pwb.Site(i, i, usr) # Atmark-chan-Bot として Incubator へ

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

# 年と週をもとに、配信元ページ名を取得して
mPageN = f'Tech/News/{y}/{w}/ja'
# ページを取得し、
mPage = pwb.Page(meta, mPageN)
# 中身のソースと
txt = mPage.text
# REVISIONID を取得したら
id = mPage.latest_revision_id
# ソースのうち Tech News 本体部分を抜き出す
m = re.search(r'<section begin="[^"]*"\/>[\s\S]*<section end="[^"]*"\/>', txt)
mainTxt = m.group()

# 投稿する文字列を生成
addTxt \
    # 改行 × 2
  = '\n\n' \
    # 節見出し
   f'== [[m:Special:MyLanguage/Tech/News/{y}/{w}|Tech News: {y}-{w}]] ==' \
    # 改行 × 2
    '\n\n' \
    # 先ほど抜き出した文字列
   f'{mainTxt}' \
    # 改行 × 2
    '\n\n' \
    # 水平線
   '----' \
    # 改行
    '\n' \
    # 追記部分
   f'[[m:{mPageN}]]<span style="font-size:smaller;">（[[m:Special:Permalink/{id}|固定]]）</span>より。--~~~~'

############################################################

  ##### 配信先ページ取得～編集 #####

# 配信先ページ取得
iPage = pwb.Page(incub, 'Wy/ja/Wikivoyage:お知らせ')
# 先ほどの文字列を最下部に足して
iPage.text += addTxt
# 要約欄の文字列を生成したら
summ = f'/* Tech News: {y}-{w} */ [[m:Special:MyLanguage/Tech/News|Tech News]] 配信。[[m:{mPageN}]]（[[m:Special:Permalink/{id}|固定]]）より'
# 投稿する
iPage.save(summary = summ, minor = False)