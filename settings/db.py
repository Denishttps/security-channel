import sqlite3

class UserDB:
  def __init__(self):
    self.conn = sqlite3.connect("bot.db")
    self.cursor = self.conn.cursor()
    self.cursor.execute('''
  CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, username TEXT, full_name TEXT)''')
    self.conn.commit()

  def get_all_users_count(self) -> int:
    self.cursor.execute("SELECT COUNT(*) FROM users")
    return self.cursor.fetchall()

  def add_user(self, user_id: int, username: str, full_name: str):
    self.cursor.execute("INSERT INTO users (user_id, username, full_name) VALUES (?,?,?)", (user_id, username, full_name))
    self.conn.commit()
    return True

  def get_user(self, username="", user_id=0):
    if username:
      self.cursor.execute("SELECT * FROM users WHERE username=?", (username,))
    else:
      self.cursor.execute("SELECT * FROM users WHERE user_id=?", (user_id,))  
    return self.cursor.fetchall()

  def del_user(self, user_id):
    self.cursor.execute("DELETE FROM users WHERE user_id=?", (user_id,))
    self.conn.commit()
    
  def __enter__(self):
    return self

  def __exit__(self, exc_type, exc_value, traceback):
    self.conn.commit()
    if self.conn:
      self.conn.close()