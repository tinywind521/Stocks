import pymysql
from warnings import filterwarnings
filterwarnings('ignore', category=pymysql.Warning)


class QueryException(Exception):
    """
    """
    pass


class ConnectionException(Exception):
    """
    """
    pass


class MySQL:
    """
    数据库连接类
    func: 基于pymysql的数据库交互类，支持事务提交和回滚，返回结果记录行数，和insert的最新id

    下面注释是config的解释。
    """

    """
    Establish a connection to the MySQL database. Accepts several
    arguments:

    host: Host where the database server is located
    user: Username to log in as
    password: Password to use.
    database: Database to use, None to not use a particular one.
    port: MySQL port to use, default is usually OK. (default: 3306)
    bind_address: When the client has multiple network interfaces, specify
    the interface from which to connect to the host. Argument can be
    a hostname or an IP address.
    unix_socket: Optionally, you can use a unix socket rather than TCP/IP.
    charset: Charset you want to use.
    sql_mode: Default SQL_MODE to use.
    read_default_file:
    Specifies  my.cnf file to read these parameters from under the [client] section.
    conv:
    Conversion dictionary to use instead of the default one.
    This is used to provide custom marshalling and unmarshaling of types.
    See converters.
    use_unicode:
    Whether or not to default to unicode strings.
    This option defaults to true for Py3k.
    client_flag: Custom flags to send to MySQL. Find potential values in constants.CLIENT.
    cursorclass: Custom cursor class to use.
    init_command: Initial SQL statement to run when connection is established.
    connect_timeout: Timeout before throwing an exception when connecting.
    (default: 10, min: 1, max: 31536000)
    ssl:
    A dict of arguments similar to mysql_ssl_set()'s parameters.
    For now the capath and cipher arguments are not supported.
    read_default_group: Group to read from in the configuration file.
    compress; Not supported
    named_pipe: Not supported
    autocommit: Autocommit mode. None means use server default. (default: False)
    local_infile: Boolean to enable the use of LOAD DATA LOCAL command. (default: False)
    max_allowed_packet: Max size of packet sent to server in bytes. (default: 16MB)
    Only used to limit size of "LOAD LOCAL INFILE" data packet smaller than default (16KB).
    defer_connect: Don't explicitly connect on contruction - wait for connect call.
    (default: False)
    auth_plugin_map: A dict of plugin names to a class that processes that plugin.
    The class will take the Connection object as the argument to the constructor.
    The class needs an authenticate method taking an authentication packet as
    an argument.  For the dialog plugin, a prompt(echo, prompt) method can be used
    (if no authenticate method) for returning a string from the user. (experimental)
    db: Alias for database. (for compatibility to MySQLdb)
    passwd: Alias for password. (for compatibility to MySQLdb)
    """

    def __init__(self, SQL_config=None):
        if SQL_config:
            self.config = SQL_config
        else:
            self.config = {
                'host': 'localhost',
                'user': 'root',
                'password': 'star2249',
                'database': 'stocks',
                'port': 3306,
                'charset': 'utf8',
                'use_unicode': None,
                'client_flag': 0,
                'cursorclass': pymysql.cursors.DictCursor,
                'connect_timeout': '600',
                'remote': False,
                'init_command': None,
                'max_allowed_packet': 16*1024*1024,
            }
        self.__conn = None
        self.__cursor = None
        self.lastrowid = None
        self.rows_affected = 0
        self.dbReturn = None
        # self.connect_timeout = connect_timeout
        # self.ip = ip
        # self.port = port
        # self.user = user
        # self.password = password
        # self.mysocket = socket
        # self.remote = remote
        # self.db = dbname


    # 内部方法，初始化连接
    def __init_conn(self):
        try:
            conn = pymysql.connect(**self.config)
        except pymysql.Error as er:
            raise ConnectionException(er)
        self.__conn = conn


    # 内部方法，初始化cursor
    def __init_cursor(self):
        if self.__conn:
            self.__cursor = self.__conn.cursor(pymysql.cursors.DictCursor)


    # 方法，关闭并复位连接
    def close(self):
        if self.__conn:
            self.__conn.close()
            self.__conn = None


    # 专门处理select语句
    def execSQL(self, sql, args=None):
        try:
            self.dbReturn = None
            if self.__conn is None:
                self.__init_conn()
                self.__init_cursor()
            self.__conn.autocommit = True
            self.__cursor.execute(sql, args)
            self.rows_affected = self.__cursor.rowcount
            results = self.__cursor.fetchall()
            self.dbReturn = results
            return results
        except pymysql.Error as er:
            raise pymysql.Error(er)
        finally:
            if self.__conn:
                self.close()


    # 专门处理dml语句 delete，update，insert和replace
    def execTXSQL(self, sql, args=None):
        try:
            if self.__conn is None:
                self.__init_conn()
                self.__init_cursor()
            if self.__cursor is None:
                self.__init_cursor()
            self.rows_affected = self.__cursor.execute(sql, args)
            self.lastrowid = self.__cursor.lastrowid
            return self.rows_affected
        except pymysql.Error as er:
            raise pymysql.Error(er)
        finally:
            if self.__cursor:
                self.__cursor.close()
                self.__cursor = None


    # 提交
    def commit(self):
        try:
            if self.__conn:
                self.__conn.commit()
        except pymysql.Error as er:
            raise pymysql.Error(er)
        finally:
            if self.__conn:
                self.close()


    # 回滚操作
    def rollBack(self):
        try:
            if self.__conn:
                self.__conn.rollback()
        except pymysql.Error as er:
            raise pymysql.Error(er)
        finally:
            if self.__conn:
                self.close()


    # 适用于需要获取插入记录的主键自增id
    def getLastRowID(self):
        return self.lastrowid


    # 获取dml操作影响的行数
    def getAffectRows(self):
        return self.rows_affected


    # MySQL_Utils初始化的实例销毁之后，自动提交
    def __del__(self):
        self.commit()
