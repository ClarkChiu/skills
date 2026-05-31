# 用Python寫一個爬蟲

最近在學爬蟲,我用requests跟BeautifulSoup這兩個套件,寫了一個小程序.其實很簡單,大概50行code就搞定了。

## 安裝

先用pip install requests安裝,版本我裝的是2.31.0.然後在terminal執行python3 main.py就可以跑了。

老闆說:"這個東西很有用,記得寫個README放到github上面"。我想說好喔,反正也不難。

## 注意事項

1. 記得設置User-Agent,不然有些網站會擋
2. 視頻網站通常需要額外處理,因為內容是動態加載的
3. 軟件版本如果不對(像是Python2跟Python3),可能會有問題

詳細的程式碼放在src/spider.py裡面,大家可以參考看看!
