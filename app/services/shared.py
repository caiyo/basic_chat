import uuid
import hashlib
import base64
import pymysql.cursors
import pymysql

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
    finally:
        connection.close()