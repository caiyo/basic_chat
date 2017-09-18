# Requirements

python 2

mysql


# Application setup

`cd <path to>/basic_chat`

`. setup.sh <mysql user>`

If you use a mysql user other than `root` you have to the config in edit `<path to>/basic_chat/app/__init.py`

change

```
app.config['DB_USER'] = 'root'
```

to

```
app.config['DB_USER'] = <mysql user>
```

Run application:

```
python run.py
```

