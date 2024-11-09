# AIWolfNLAgentPython

人狼知能コンテスト2024冬季国内大会（自然言語部門）のPythonによるサンプルエージェントです。  
エージェントと対戦接続システムと接続するためのものです。  
大会についての詳細は、https://sites.google.com/view/aiwolfdial2024winterjp/ をご覧ください。  
ローカル内で動作確認ならびに自己対戦するための対戦接続システムは、https://github.com/aiwolfdial/AIWolfNLPServer をご覧ください。  

## 概要

エージェントは参加者ご自身のマシンで実行する必要があります。そのため、エージェントの実装については実装言語を含め、制限はありません。  
自己対戦の際は、5体のエージェントを固定IP/ポートにてリモート待ち受け状態にし、対戦接続システムを実行することで対戦を行います。  

`全エージェント共通`の動作には`player/agent.py` が呼び出されますので、`talk`,`vote`関数をカスタマイズしてお使いください。  
`村人専用`の動作には`player/agent.py`を継承した`player/villager.py`が呼び出されますので、`talk`,`vote`関数をカスタマイズしてお使いください。  
`占い師専用`の動作には`player/agent.py`を継承した`player/seer.py`が呼び出されますので、`divine`関数や`talk`,`vote`関数をカスタマイズしてお使いください。  
`狂人専用`の動作には`player/agent.py`を継承した`player/possessed.py`が呼び出されますので、`talk`,`vote`関数をカスタマイズしてお使いください。  
`人狼専用`の動作には`player/agent.py`を継承した`player/werewolf.py`が呼び出されますので、`attack`関数や`talk`,`vote`関数をカスタマイズしてお使いください。

## 参加登録

https://sites.google.com/view/aiwolfdial2024winterjp/ をご覧ください。

## 環境構築

```
$ git clone https://github.com/aiwolfdial/AIWolfNLAgentPython
$ cd AIWolfNLAgentPython
$ python -m venv .venv
$ source .venv/bin/activate
$ pip install aiwolf-nlp-common
$ pip install -r res/requirements.txt
```

> [!WARNING]
> aiwolf-nlp-common >= 0.0.2.1 であることを確認してください。\
> `pip install aiwolf-nlp-common` に失敗する場合は、以下のURLを参照してください。
> https://pypi.org/project/aiwolf-nlp-common/

### aiwolf-nlp-commonパッケージについて

役職や接続方式に関するプログラムが定義されているPythonパッケージです。  
詳細については、https://github.com/aiwolfdial/AIWolfNLPCommon をご覧ください。

## 自己対戦

1. `res/config.ini.sample`を`res/config.ini`に名前を変更してください。
1. 以下のコマンドを実行してください。
	```
	$ python multiprocess.py
	```
1. 対戦接続システムを起動してください。\
	対戦接続システムは、https://github.com/aiwolfdial/AIWolfNLPServer をご覧ください。

### 主催者が提供するサーバでの自己対戦の実行

> [!WARNING]
> 人狼知能コンテスト2024冬季国内大会から新しい対戦接続システムに置き換える予定であるため、以下の手順とは異なります。
> 新しい対戦接続システムについて決まり次第、こちらに記載します。

ここでは参加者の方々に対戦サーバの待ち受けができているか確認する方法を説明します。

1. `res/config.ini`の設定を行ってください。
	以下の値は変更を行わないでください。
	```	
	[game]
	num = 1
	```
2. `res/ssh-config`の設定を行ってください。
3. 最後にエージェントのプログラムを実行してください
	```
	$ python multiprocess.py
	```
4. エージェントが待ち受けているポート番号を運営が提供するするサーバの対戦プログラムに伝える。
	[AIWolfPreliminaryRun](https://github.com/aiwolfdial/AIWolfPreliminaryRun)の内容に従ってAIWolfPreliminaryRunのプログラムを実行してください。

### 本戦での実行

> [!WARNING]
> 人狼知能コンテスト2024冬季国内大会から新しい対戦接続システムに置き換える予定であるため、以下の手順とは異なります。
> 新しい対戦接続システムについて決まり次第、こちらに記載します。

1. `res/config.ini`の設定を行ってください。
	以下の値は当日の運営の指示に従い設定してください。
	```	
	[game]
	num = ???

	[agent]
	num = ???
	```
1. エージェントプログラムの実行
	```
	$ python multiprocess.py
	```

## 設定

`res/config.ini.sample` を `res/config.ini` に名前を変更してください。  

### [connection]

`host_flag`: trueの場合に対戦接続の待ち受けを行います。 falseの場合はゲームサーバへの接続を行います。  
`ssh_flag`: trueの場合に運営が提供するサーバへSSH接続をプログラムから行います。 falseの場合はSSH接続ではなく2023年以前のようにTCPコネクションを行います。  
`buffer`: 対戦サーバとの送受信の際に利用されるバッファサイズです。  
`keep_connection`: **本戦の場合のみ** `true`にしてください。

### [tcp-client]

**過去のシステムとの互換性設定のため、大会参加時には変更の必要はありません。ローカルで自己対戦を行う際に使用します。**  
`host`:2023年までの接続方式です。後述する`execute.sh`で使用しているため対戦サーバにSSHで接続される場合はデフォルトで設定をしてください。`ssh_flag=false`かつ`host_flag=false`の時に対戦サーバに接続するTCPクライアントとして動作します。

### [game]

`num`: 連続で行うゲームの回数です。

### [agent]

`num`: ゲームに参加するエージェントの人数です。  
`name*`: *番目のエージェントの名前です。

```
[connection]
host_flag = true
ssh_flag = true
buffer = 2048

[ssh-server]
config_path = ./res/ssh-config
host_name = aiwolf-server
ssh_agent_flag = true
timeout = 200

[tcp-client]
; local sever settings
host = localhost
port = 10001

[game]
num = 1

[agent]
num = 5
name1 = kanolab1
```

## ログの設定

`res/log.ini.sample` を `res/log.ini` に名前を変更してください。  

`storage_path`: エージェントのログを保存するパスの設定です

`get_info`\
`true`:ゲームサーバから取得したJsonをログに書き込みます。\
`false`:ログに書きません。

`initialize` = true\
`true`:initializeリクエストの時にゲームサーバから取得したJsonをログに書き込みます。\
`false`:ログに書きません。

`talk`\
`true`:エージェントがゲームサーバに送信した`TALK`の内容ををログに書き込みます。\
`false`:ログに書きません。

`vote`\
`true`:エージェントがゲームサーバに送信した`VOTE`の内容ををログに書き込みます。\
`false`:ログに書きません。

`divine`\
`true`:エージェントがゲームサーバに送信した`DIVINE`の内容ををログに書き込みます。\
`false`:ログに書きません。

`divine_result`\
`true`:ゲームサーバから取得した占いの結果をログに書き込みます。\
`false`:ログに書きません。

`attack`\
`true`:エージェントがゲームサーバに送信した`ATTACK`の内容ををログに書き込みます。\
`false`:ログに書きません。
