"""
Orthobest Care Hub - Package Initialization.
Ensures seamless MariaDB / MySQL connectivity on shared hosting using PyMySQL or mysqlclient.
"""
try:
    import pymysql
    pymysql.install_as_MySQLdb()
except ImportError:
    pass
