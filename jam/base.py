import enum


class Operation(enum.IntEnum):
    CREATE = 0
    UPDATE = 1
    REPLACE = 2
    DELETE = 3
    SNAPSHOT = 4
    RENAME = 5
