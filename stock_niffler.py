import time
import json
import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta


class STOCK_NIFFLER:
    def _collect_stock(self, days_ago):
        print(f"開始收集近 {days_ago} 日股市資訊")
        day_searched = 0
        today = datetime.now()
        stocks = {}
        dates = []
        url = "http://www.twse.com.tw/exchangeReport/MI_INDEX"
        query_params = {
            "date": "",
            "response": "json",
            "type": "ALL",
        }
        while day_searched < int(days_ago):
            date = today.strftime("%Y%m%d")
            today = today + timedelta(days=-1)
            query_params["date"] = date
            try:
                page = requests.get(url, params=query_params)
            except:
                page = []
                print(f"{date} 尚未收盤，請稍後再試。")
                break
            time.sleep(5)
            if page and page.json()["stat"] == "OK":
                day_searched += 1
                dates.append(date)
                print(f"{date} added")
                if day_searched == 10:
                    time.sleep(10)
                for stock in page.json()["data9"]:
                    if stock[0] not in stocks:
                        try:
                            stocks[stock[0]] = {
                                "name": stock[1],
                                "price": [float(stock[8])],
                                "volume": [int(stock[2].replace(",", ""))],
                            }
                        except:
                            pass
                    else:
                        try:
                            stocks[stock[0]]["price"].append(float(stock[8]))
                            stocks[stock[0]]["volume"].append(
                                int(stock[2].replace(",", ""))
                            )
                        except:
                            del stocks[stock[0]]
        return stocks, dates

    def stock_rank(self, stocks):
        for k, v in stocks.items():
            v["rising"] = round(
                ((v["price"][0] - v["price"][-1]) / v["price"][-1]) * 100, 2
            )
        sort_stocks = sorted(stocks.items(), key=lambda x: x[1]["rising"], reverse=True)
        listed_stocks = {}
        for item in sort_stocks:
            if len(item[0]) == 4:
                listed_stocks[item[0]] = item[1]
        print("*****\n所有股票漲幅 top 5 :")
        for idx in range(5):
            print(
                f"{sort_stocks[idx][0]} {sort_stocks[idx][1]['name']} {sort_stocks[idx][1]['rising']}%({sort_stocks[idx][1]['price'][-1]}→{sort_stocks[idx][1]['price'][0]})"
            )
        print("*****\n上市(櫃)股票漲幅 top 5 :")
        listed_stocks = list(listed_stocks.items())
        for idx in range(5):
            print(
                f"{listed_stocks[idx][0]} {listed_stocks[idx][1]['name']} {listed_stocks[idx][1]['rising']}%({listed_stocks[idx][1]['price'][-1]}→{listed_stocks[idx][1]['price'][0]})"
            )
        return ""

    def draw(self, data, number, price_volume, dates):
        plt.figure(figsize=(15, 8))
        plt.style.use("fivethirtyeight")
        price_volume_str = []
        price_volumes = data[str(number)][price_volume][::-1]
        dates = dates[::-1]
        for idx in range(len(dates)):
            price_volume_str.append(f"{dates[idx]}\n{price_volumes[idx]}")
        colors = {"price": "R", "volume": "B"}
        print(
            f"{number} {data[number]['name']} 近 {len(dates)} 日 {price_volume} 為 :\n {price_volumes}"
        )
        plt.plot(price_volume_str, price_volumes, color=colors[price_volume])
        plt.xticks(fontsize=5)
        plt.yticks(fontsize=5)
        plt.xlabel("day", fontsize=8)
        plt.show()


if __name__ == "__main__":
    niffler = STOCK_NIFFLER()
    days_ago = input("你想蒐集前幾天的資訊 ?")
    data, dates = niffler._collect_stock(days_ago)
    # 列出漲幅 top 5
    if data:
        niffler.stock_rank(data)
        while True:
            number = input("你想查哪支股票(代號) ? ")
            price_volume = input("你想查股價還是交易量 ? (輸入 price 或volume) ?")
            niffler.draw(data, number, price_volume, dates)
