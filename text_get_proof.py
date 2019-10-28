from requests_html import HTMLSession

## CONSTANT
apikey = "{YOUR_API_KEY}"
endpoint = "https://api.a3rt.recruit-tech.co.jp/proofreading/v2/typo"
sensitivity = "medium"

# UAの定義（デフォルトから変更する場合）
headers = {'User-Agent':'test'}
## Default
# Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/603.3.8 (KHTML, like Gecko) Version/10.1.2 Safari/603.3.8

session = HTMLSession()

# Yahoo!ニュースの主要ニュースの見出しを出力
r = session.get("https://news.yahoo.co.jp/", headers = headers)
items = r.html.find(".topicsListItem", first=False)

for item in items:
    # 重複を除くためset型で返されるのでlistに変換しておく
    link = list(item.absolute_links)
    
    # 詳細ページをレンダリング
    r_detail = session.get(link[0], headers = headers)

    # 詳細ページの概要を表示
    item_detail = r_detail.html.find(".tpcNews_summary", first=True)

    # 詳細ページの概要をA3RT「ProofreadingAPI」で文章をチェック
    sentence = item_detail.text
    params = {'apikey': apikey,
              'sentence': sentence,
              'sensitivity': sensitivity,
            }
    response = session.get(endpoint, headers = headers, params= params)
    print(response.json()["checkedSentence"])
    print("--")
    print(item_detail.text)
    print("----------")
