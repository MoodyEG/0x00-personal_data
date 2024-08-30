#!/usr/bin/env python3
""" Obduscated log messages """
import logging
import re
from typing import List
import os
import mysql.connector
import subprocess


def get_db() -> mysql.connector.connection.MySQLConnection:
    """ Get a connection to the database """
    with open("mysql_update.sh", "w") as f:
        f.write("""#!/bin/bash
        mysql -u root -e "USE mysql; UPDATE user SET \
        plugin='mysql_native_password' \
        WHERE User='root'; FLUSH PRIVILEGES;"
        service mysql restart
        """)
    subprocess.run(["bash", "mysql_update.sh"])

    connection = mysql.connector.connect(
        user=os.getenv("PERSONAL_DATA_DB_USERNAME", "root"),
        password=os.getenv("PERSONAL_DATA_DB_PASSWORD", ""),
        host=os.getenv("PERSONAL_DATA_DB_HOST", "localhost"),
        database=os.getenv("PERSONAL_DATA_DB_NAME")
    )
    return connection


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    """ Return a configured logger """
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(handler)
    return logger


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """ Filter_datum """
    for field in fields:
        message = re.sub(f"{field}=[^{separator}]*",
                         f"{field}={redaction}", message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Constructor """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """ Format method """
        return filter_datum(self.fields, self.REDACTION,
                            logging.Formatter.format(self, record),
                            self.SEPARATOR)


def main():
    """ Main function """
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    headers = [field[0] for field in cursor.description]
    logger = get_logger()
    for row in cursor:
        info_answer = ""
        for f, p in zip(row, headers):
            info_answer += f"{p}={f}; "
        logger.info(info_answer)
    cursor.close()
    db.close()


if __name__ == "__main__":
    main()
