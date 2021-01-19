import os
import sys

import psycopg2 as dbapi2

INIT_STATEMENTS = [
	
	"""CREATE TABLE IF NOT EXISTS USERS (
        USER_ID		BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
        USER_EMAIL	VARCHAR(50) UNIQUE NOT NULL,
        USERNAME	VARCHAR(20) UNIQUE NOT NULL,
        PASSWORD	VARCHAR(30) NOT NULL,
        IS_ADMIN    BOOLEAN DEFAULT FALSE
    )""",
	"""CREATE TABLE IF NOT EXISTS DONORS (
		DONOR_ID	BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
		NAME		VARCHAR(100) NOT NULL,
		SURNAME		VARCHAR(100) NOT NULL,
		PHONE_NUMBER	BIGINT NOT NULL,
		BIRTH_DATE	VARCHAR(20) NOT NULL,
		BLOOD_TYPE	VARCHAR(20) NOT NULL,
		ADDRESS		VARCHAR(300),
		LAST_DONATE_DATE	VARCHAR(20) DEFAULT 'Has Not donated Yet'
	)""",
	"""CREATE TABLE IF NOT EXISTS PATIENTS (
		PATIENT_ID	BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
		NAME		VARCHAR(100) NOT NULL,
		SURNAME		VARCHAR(100) NOT NULL,
		PHONE_NUMBER	BIGINT NOT NULL,
		BIRTH_DATE	VARCHAR(20) NOT NULL,
		BLOOD_TYPE	VARCHAR(20) NOT NULL,
		ADDRESS		VARCHAR(300)
	)""",
        """CREATE TABLE IF NOT EXISTS BLOODBAGS (
        BLOODBAG_ID BIGSERIAL PRIMARY KEY NOT NULL UNIQUE,
        BLOOD_TYPE  VARCHAR(20) NOT NULL,
        DONOR_ID    BIGINT,
        PATIENT_ID  BIGINT,
        EXPIRATION  VARCHAR(20) NOT NULL,
        FOREIGN KEY (DONOR_ID) REFERENCES DONORS (DONOR_ID), 
        FOREIGN KEY (PATIENT_ID) REFERENCES PATIENTS (PATIENT_ID)
    )"""
]


def initialize(url):
    with dbapi2.connect(url) as connection:
        cursor = connection.cursor()
        for statement in INIT_STATEMENTS:
            cursor.execute(statement)
            
        cursor.close()

# DATABASE_URL = 'postgres://roanqhsatcqkrw:10c97d66b5bdb32b285af396b5cef5af3c4ea1adb9994c52ab01d17a65a820ef@ec2-3-234-109-123.compute-1.amazonaws.com:5432/daaaitntb4vqkm'  #os.getenv("DATABASE_URL")
if __name__ == "__main__":
    NEW_URL = os.getenv("DATABASE_URL")
    if not NEW_URL:
        url = "postgres://postgres:test123@localhost:5432/bds"
        initialize(url)
    else:
        db.bind(provider="postgres", dsn=DATABASE_URL)
        initialize(NEW_URL)
    if url is None:
        print("Usage: DATABASE_URL=url python dbinit.py", file=sys.stderr)
        sys.exit(1)
    
