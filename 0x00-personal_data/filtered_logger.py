#!/usr/bin/env python3
'''
    Function filter_datum that returns the log message obfuscated.
'''
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
    for part in message.split(separator):
        if part.split("=")[0] in fields:
            message = re.sub(part.split("=")[1], redaction, message)
    return message
