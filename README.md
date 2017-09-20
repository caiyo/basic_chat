# Requirements

python 2

pip

npm

bower

mysql

# Install Dependencies

pip:

```
sudo easy_install pip
```

npm:

```
brew install node
```

bower:

```
npm install bower -g
```

# Application setup

`cd <path to>/basic_chat`

`. setup.sh <mysql user>`

eg:

`. setup.sh root`

If you use a mysql user other than `root` you have to the config in edit `<path to>/basic_chat/app/__init__.py`
If your user has a password, update that as well
change

```
app.config['DB_USER'] = 'root'
app.config['DB_PASSWORD'] = ''
```

to

```
app.config['DB_USER'] = <mysql user>
app.config['DB_PASSWORD'] = <mysql user passord>
```

# Run application:

activate venv:

```
. venv/bin/activate
```

Run application:

```
python run.py
```

Go to url: `127.0.0.1:5000`
