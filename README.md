## DEBIAN/UBUNTU

# redis

Prerequisites
```bash
sudo apt install lsb-release curl gpg
```

Install
```bash
curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg

echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list

sudo apt update
sudo apt install redis
```

Start
```bash
service redis-server start
```
# addok

python3 >= 3.7
```bash
sudo apt install python3 python3-dev python3-pip python3-virtualenv build-essential
```

clone the repo
```bash
git clone https://github.com/harmdhast/python-addok-dbupdate.git
cd ./python-addok-dbupdate
```

setup virtualenv
```bash
virtualenv .env
source .env/bin/activate
pip install -U pip setuptools
```

addok with cython
```bash
pip install git+https://github.com/roy-ht/editdistance.git@v0.6.2 # Missing dep fix
pip install cython
pip install --no-binary :all: falcon
pip install --no-binary :all: addok
pip install addok-fr addok-france
```

run the script : defaults to redis localhost, french adresses full
```bash
pip install -r requirements.txt
python3 ./run.py
```

test the API (in virtualenv)
```bash
addok shell --conf addok.conf
addok serve --conf addok.conf
curl "http://127.0.0.1:7878/search/?q=epinay+sur+seine"
```