#!/usr/bin/env python3
'''
    Function filter_datum that returns the log message obfuscated.
'''
import logging
import mysql.connector
import os
import re
from typing import List


def filter_datum(
        fields: List[str],
        redaction: str,
        message: str,
        separator: str
        ) -> str:
    '''
        filter_datum: function
        @fields: List of strings representing all fields to obfuscate
        @redaction: String representing by what the field will be obfuscated
        @message: String representing the log line.
        @separator: String representing by which character is separating
                    all fields in the log line (message).
        return: The log message obfuscated.
    '''
    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                         f'{field}={redaction}{separator}', message)
    return message


PII_FIELDS = ("name", "email", "phone", "ssn", "password")


def get_logger() -> logging.Logger:
    '''
        get_logger: function
        return: Logging.Logger object.
    '''
    new_logger = logging.getLogger("user_data")
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(PII_FIELDS))
    new_logger.setLevel(logging.INFO)
    new_logger.propagate = False
    new_logger.addHandler(stream_handler)
    return new_logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''
        get_db: function
        return: The mysql connector object.
    '''
    db_username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
    db_password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
    db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
    db_name = os.getenv("PERSONAL_DATA_DB_NAME", "")
    connection = mysql.connector.connect(host=db_host,
                                         port=3306,
                                         user=db_username,
                                         password=db_password,
                                         database=db_name)
    return connection


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''
            format: instance method.
            @self: class constructor.
            @record: LogRecord object.
            return: The log message.
        '''
        msg = super(RedactingFormatter, self).format(record)
        return filter_datum(self.fields, self.REDACTION, msg, self.SEPARATOR)
