import uuid
import hashlib
import base64
import pymysql.cursors
import pymysql
import json
from datetime import date, datetime


def create_salt():
    uuid_bytes = uuid.uuid4().bytes
    return b64_encode(uuid_bytes)

def hash_string(string):
    hash_str = hashlib.sha512(string).digest()
    return b64_encode(hash_str)

def b64_encode(str_):
    return base64.urlsafe_b64encode(str_)


def run_sql(sql, params=None, commit=False, fetchone = False):
    # Connect to the database
    connection = pymysql.connect(user='root',
                                 db='challenge_kyle')

    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute(sql, params)

        if commit:
            connection.commit()
        result = None

        if fetchone:
            result = cursor.fetchone()
        else:    
            result = cursor.fetchall()
        print 
        return result
    
    except Exception as e:
        print "EXCEPTION:~~~~_~~_~_~_~_"
        print "ERROR: {0}".format(e)
        print "SQL: {0}".format(sql)
        print "params: {0}".format(params)
    finally:
        connection.close()


def to_json(data):
    return json.dumps(data, cls=ComplexEncoder)


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if hasattr(obj,'reprJSON'):
            return obj.reprJSON()
        else:
            return json.JSONEncoder.default(self, obj)