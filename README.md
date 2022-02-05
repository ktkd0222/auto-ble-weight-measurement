# summary
- 体重計に自動接続及びデータを送信するPythonスクリプトです。
- BLE情報を受信したら体重を計算して、HTTPリクエストを送信可能です。

# environment
- Raspberry Pi 3 or 4

   [note] requires bluetooth module.

- Python 3.7.3 or later

# requirements
``` bash
$ sudo apt-get install python-dev libbluetooth3-dev
$ sudo apt-get install libglib2.0 libboost-python-dev libboost-thread-dev

$ sudo pip3 install -r requirements.txt
```

# install
``` bash
# clone repository
$ git clone xxxxxxxxxxx

$ cd ble-weight-measurement/scripts
$ sudo chmod +x install.sh
$ sudo ./install.sh


```