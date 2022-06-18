from pyftpdlib.handlers import FTPHandler as PYFTPHandler
from hashlib import md5
import sqlite3
import server_config
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.servers import FTPServer
from os import path, mkdir


def recursive_mkdir(given_path):
    directories = given_path.split("/")
    length = len(directories)
    given_path, start_index = ("/" + directories[1], 2) if given_path[0] == '/' else (directories[0], 1)
    if not path.isdir(given_path):
        mkdir(given_path)

    for index in range(start_index, length):
        if len(directories[index]) > 0:
            given_path = given_path + '/' + directories[index]
            if not path.isdir(given_path):
                mkdir(given_path)


class FTPHandler(PYFTPHandler):
    def __init__(self, conn, serve, ioloop=None):
        super().__init__(conn, serve, ioloop)
        self.sign_in_process = 0
        self.user_details = None
        self.files_in_transit = {}
        self.proto_cmds['SIGNIN'] = dict(perm=None, auth=False, arg=True,
                                         help='Syntax: SIGNIN (list all new features supported).')
        self.home_dir = server_config.base_dir

        if not path.isfile(server_config.database_path):
            last_slash = server_config.database_path.rindex('/')
            database_directory = server_config.database_path[0:last_slash]

            # check if directories exist and if not create them
            if not path.isdir(database_directory):
                recursive_mkdir(database_directory)

        conn = sqlite3.connect(server_config.database_path)
        cursor = conn.cursor()
        # check if tables don't exist and create them
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        if cursor.fetchall().__str__().find('user') == -1:
            conn.execute('''PRAGMA FOREIGN_KEYS = ON;''')
            conn.execute('''create table user(
                                id integer primary key autoincrement not null ,
                                username text unique not null,
                                password text not null ,
                                permissions text not null ,
                                directory text not null unique
                            );''')

            conn.execute('''create table file(
                                id integer primary key autoincrement not null,
                                file_name text not null,
                                file_path text unique not null ,
                                file_type text not null ,
                                hash_value text not null ,
                                user integer not null ,
                                foreign key (user) references user(id)
                            );''')
            conn.commit()
        conn.close()

    def ftp_SIGNIN(self, args):
        self.sign_in_process = 1
        arr = args.split(' ')
        credentials = ['', '']
        pos = -1
        for string in arr:
            if len(string) > 0:
                if pos > -1:
                    credentials[pos] = string
                    pos = -1
                elif string == '-u':
                    pos = 0
                elif string == '-p':
                    pos = 1
        directory = self.home_dir + credentials[0]
        permissions = 'elradfmwMT'
        insert_value = self.add_user_to_db(credentials[0], credentials[1], directory, permissions)
        if insert_value == 1:
            if not path.isdir(directory):
                recursive_mkdir(directory)
            self.authorizer.add_user(credentials[0], credentials[1], directory, permissions)
            self.respond('220 sign up successful')
        else:
            self.respond('221 user exists')

    def ftp_USER(self, line):
        self.username = line
        self.user_details = self.fetch_user(self.username)

        if self.user_details is not None:
            if self.authenticated:
                self.flush_account()
            if self.sign_in_process == 0:
                self.respond('331 Username ok, send password.')
        else:
            self.username = None
            self.respond("543 User does not exist.")

    def ftp_PASS(self, line):
        if self.authenticated:
            self.respond("503 User already authenticated.")
            return
        if not self.username:
            self.respond("503 Login with USER first.")
            return

        if self.user_details['password'] == line:
            if self.authorizer.has_user(self.username):
                self.authorizer.remove_user(self.username)
            self.authorizer.add_user(self.username, line, self.user_details['directory'],
                                     self.user_details['permissions'])
            home = self.authorizer.get_home_dir(self.username)
            msg_login = self.authorizer.get_msg_login(self.username)
            self.handle_auth_success(home, line, msg_login)
        else:
            self.handle_auth_failed('Wrong password', line)

    def on_logout(self, username):
        self.authorizer.remove_user(username)

    @staticmethod
    def fetch_user(username):
        if path.isfile(server_config.database_path):
            conn = sqlite3.connect(server_config.database_path, detect_types=sqlite3.PARSE_COLNAMES)
            conn.row_factory = sqlite3.Row

            cursor = conn.cursor()
            cursor_obj = cursor.execute("select * from user where username='" + username + "';")
            user_row = cursor_obj.fetchone()
            user_dict = user_row if user_row is None else dict(user_row)
            conn.close()
            return user_dict
        return None

    def on_file_received(self, file):
        hash_value = md5(open(file, 'rb').read()).hexdigest()
        self.add_file_to_db(path.basename(file), file, self.files_in_transit[file][0], hash_value)
        if hash_value == self.files_in_transit[file][1]:
            self.respond("230 r=1")
        else:
            self.respond("230 r=0")
        del self.files_in_transit[file]

    def ftp_STOR(self, file, mode='w'):
        param_index = file.find('|>')
        params = file[param_index + 2:].split('|')
        file_dir = self.user_details['directory'] + (server_config.user_image_dir if params[0] == 'image' else
                                                     (server_config.user_audio_dir if params[0] == 'audio'
                                                      else server_config.user_video_dir))
        recursive_mkdir(file_dir)
        file_path = file_dir + file[0:param_index].split('/')[-1]
        self.files_in_transit[file_path] = params
        super().ftp_STOR(file_path, mode)

    @staticmethod
    def add_user_to_db(username, password, directory, permissions):
        conn = sqlite3.connect(server_config.database_path)
        try:
            conn.execute("insert into user (username, password, permissions, directory) values (?,?,?,?)",
                         (username, password, permissions, directory))
            conn.commit()
            conn.close()
            return 1
        except sqlite3.IntegrityError:
            conn.close()
            return -1

    def add_file_to_db(self, file_name, file_path, file_type, file_hash):
        conn = sqlite3.connect(server_config.database_path)
        try:
            conn.execute("insert into file(file_name, file_path, file_type, hash_value, user) values (?,?,?,?,?)",
                         (file_name, file_path, file_type, file_hash, self.user_details['id']))
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            conn.execute("update file set file_name=?, hash_value=? where file_path=?",
                         (file_name, file_hash, file_path))
            conn.commit()
            conn.close()


if __name__ == "__main__":
    authorizer = DummyAuthorizer()
    handler = FTPHandler
    handler.authorizer = authorizer

    # Define a customized banner (string returned when client connects)
    handler.banner = "Hello, welcome to team one ftp server"

    server = FTPServer((server_config.address, server_config.port), FTPHandler)
    server.serve_forever()
