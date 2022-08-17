import time
n = 50                   # 設定進度條總長
for i in range(n+1):
    print(f'\r[{"█"*i}{" "*(n-i)}] {i*100/n}%', end='')   # 輸出不換行的內容
    time.sleep(0.5)