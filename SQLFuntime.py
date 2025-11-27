import os
import psycopg2
import time
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from passlib.context import CryptContext
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")  # we'll set this in .env

DATABASE_URL = os.environ["DATABASE_URL"]
if "?sslmode=" not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require"

def require_ssl(u: str) -> str:
    p = urlparse(u)
    q = dict(parse_qsl(p.query))
    q.setdefault("sslmode", "require")
    return urlunparse(p._replace(query=urlencode(q)))

conn1 = psycopg2.connect(DATABASE_URL)
cur1 = conn1.cursor()


def get_connection():
    return psycopg2.connect(require_ssl(DATABASE_URL))




def find_numbers(): 
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT * FROM numbers
        """,
    )
    rows = cur.fetchall()
    conn.close()
    return rows



def insert_message(num, message):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE numbers SET messages = array_append(messages, %s) WHERE number = %s
        """, (message,  str(num))
    )
    updated = cur.rowcount
    conn.commit()
    conn.close()
    if updated == 0:
        return False
    else:
        return True

def get_messages(num):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT messages FROM numbers where number = %s
        """, (str(num),)
    )
    row = cur.fetchall()
    conn.close()
    #print(row)
    flat = [msg for (inner,) in row for msg in inner]
    return flat



def create_number(num, message):
    conn = get_connection()
    cur = conn.cursor()
    id = int(time.time() * 1000)
    cur.execute(
        """
        INSERT INTO numbers (id, number, messages) VALUES (%s, %s, %s)
        """, (id,  "+1" + str(num), [message])
    )
    # row = cur.fetchone()
    print("ROOOOW")
    # print(row)
    conn.commit()
    conn.close()

    return True

def delete_number(number):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        DELETE FROM numbers
        WHERE number = %s
        """,
        (number,)   # parameters must be a tuple
    )
    conn.commit()  # IMPORTANT
    conn.close()


def get_number_or_create_number(num, message):
    print("\n\n\n\n" + str(num) + "\n\n\n\n")
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT messages FROM numbers where number = %s
        """, ( str(num),)
    )
    row = cur.fetchall()
    if row == None:
        create_number(num, message)
    
        cur.execute(
        """
        SELECT messages FROM numbers where number = %s
        """, ( str(num),)
        )
        row = cur.fetchall()
        conn.close()
        return row
    else:
        conn.close()
        return row
    
def resetNumber(num):
    message = ["Sarah: It’s Sarah from Meridian Health. Is this the same Kevin that got a quote from us in the last couple of months?"]
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE numbers SET messages = %s WHERE number = %s",
        (message, "+1" + str(num),)
    )
    conn.commit()
    conn.close()

    return True


#Amins
def create_admin(email, password, prompt):
    conn = get_connection()
    cur = conn.cursor()
    id = int(time.time() * 1000)
    hashed_password = pwd_context.hash(password)
    cur.execute(
        """
        INSERT INTO administrators VALUES (%s, %s, %s, %s)
        """, (id, email, hashed_password, prompt)
        )
    conn.commit()
    conn.close()

    return True


def get_admin(email, password):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute(
        """
        SELECT * FROM administrators where email = %s
        """, (email,)
        )
    row = cur.fetchall()
    print(row)
    stored_hash = row[0][2]

    if not pwd_context.verify(password, stored_hash):
        print("invalid password")
        raise HTTPException(401, "invalid credentials")

    conn.commit()
    conn.close()
    return row

def get_admin_By_Id(id):
    conn = get_connection()
    cur = conn.cursor()
    
    cur.execute(
        """
        SELECT * FROM administrators where id = %s
        """, (id,)
        )
    row = cur.fetchall()

    conn.commit()
    conn.close()
    return row

def checkEmail(email):
    #print(name)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT email FROM administrators WHERE email = %s",
        (email,))
    row = cur.fetchall()
    conn.commit()
    conn.close()
    print(row)

    if row is None or len(row) !=0:
        print("Twas false")
        return False
    else:
        return True
    
def getPrompt(email):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT prompt FROM administrators WHERE email = %s",
        (email,))
    row = cur.fetchall()
    conn.commit()
    conn.close()
    print(row)

    if row is None or len(row) !=0:
        print("Twas false")
        return False
    else:
        return True   

def updatePrompt(email, prompt):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE administrators SET prompt = %s WHERE email = %s",
        (prompt, email))
    conn.commit()
    conn.close()

    return True

        
        
#print(get_messages("+1777"))
#print(insert_message(7256001255, "."))



