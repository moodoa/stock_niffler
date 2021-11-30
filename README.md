# stock_niffler
蒐集近 X 日的股市資訊

![alt text](https://sigortagazetesi.com/wp-content/uploads/2021/11/endeks.jpg)

## stock_niffler.py
* 從台灣證交所 (TWSE) 上蒐集近 X 日股市資訊並繪製圖表。

## Requirements
python 3.7

## Installation
`pip install -r requriements.txt`

## usage
```
if __name__ == "__main__":
    niffler = STOCK_NIFFLER()
    days_ago = input("你想蒐集前幾天的資訊 ?")
    data, dates = niffler._collect_stock(days_ago)
    # 列出漲幅 top 5
    niffler.stock_rank(data)
    while True:
        number = input("你想查哪支股票(代號) ? ")
        price_volume = input("你想查股價還是交易量 ? (輸入 price 或volume) ?")
        niffler.draw(data, number, price_volume, dates)
```