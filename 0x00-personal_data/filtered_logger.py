#!/usr/bin/env python3
"""filter_datum function"""

from typing import List
import re
import logging
import mysql.connector
from os


PII_FIELDS = ('name', 'password', 'phone', 'ssn', 'email')


def filter_datum(
        fields: List[str],
        redaction: str, message: str, separator: str
        ) -> str:
    """_summary_

    Args:
        fields (List[str]): _description_
        redaction (str): _description_
        message (str): _description_
        separator (str): _description_

    Returns:
        str: _description_
    """

    for i in fields:
        message = re.sub(i + "=.*?" + separator,
                         i + "=" + redaction + separator,
                         message)
    return message


class RedactingFormatter(logging.Formatter):
    """_summary_

    Args:
        logging (_type_): _description_

    Returns:
        _type_: _description_
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """Constructor method"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Filters values in incoming log records using filter_datum"""
        return filter_datum(self.fields, self.REDACTION,
                            super(RedactingFormatter, self).format(record),
                            self.SEPARATOR)


def get_logger() -> logging.Logger:
    """_summary_

    Returns:
        logging.Logger: _description_
    """

    log = logging.getLogger('user_data')
    log.setLevel(logging.INFO)
    log.propagate = False
    stream_h = logging.StreamHandler()
    formatter = RedactingFormatter(PII_FIELDS)
    log.setFormatter(formatter)
    log.addHandler(stream_h)

    return log


def get_db() -> mysql.connector.connection.MySQLConnection:
    """Returns a connection to the database."""

    db_connection = mysql.connector.connect(
        user=os.getenv('PERSONAL_DATA_DB_USERNAME', 'root'),
        password=os.getenv('PERSONAL_DATA_DB_PASSWORD', ''),
        host=os.getenv('PERSONAL_DATA_DB_HOST', 'localhost'),
        database=os.getenv('PERSONAL_DATA_DB_NAME')
    )

    return db_connection


def main():
    """_summary_
    """
    my_db = get_db()
    cursor = my_db.cursor()
    cursor.execute("SELECT * FROM users;")
    fields = [i[0] for i in cursor.description]

    log = get_logger()

    for row in cursor:
        _row = ''.join(f'{f}={str(r)}; ' for r, f in zip(row, fields))
        log.info(_row.strip())

    cursor.close()
    my_db.close()
