# sort-riddle-v2

## sort-riddle-v2

ソートなぞなぞを遊べるDiscord Bot です。2代目になります

## ソートなぞなぞとは

`''.join(sorted(list(X)))` が与えられるので、`X` を推測する遊びです

## コマンド
- !start  
    ゲームを開始します
- !answer 文字列  
  文字列が答えかどうか判定します
- !hint  
  答えの1文字目を表示します
- !giveup  
    ギブアップ用のコマンドです


## 招待リンク
https://discord.com/api/oauth2/authorize?client_id=761582339557556245&permissions=2048&scope=bot

## 起動方法(自分で建てたい人へ)
```bash
$ git clone https://github.com/t4t5u0/sort-riddle-v2.git
$ cd sort-riddle-v2
$ echo -e '[TOKEN]\ntoken=Botのシークレットトークン' > config.ini
$ pip install -r requirements.txt
$ nohup python main.py &
```