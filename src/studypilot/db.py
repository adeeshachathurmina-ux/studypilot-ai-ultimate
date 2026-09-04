import sqlite3,hashlib,secrets
DB='studypilot.db'
def c():
 x=sqlite3.connect(DB);x.execute('CREATE TABLE IF NOT EXISTS users(u TEXT PRIMARY KEY,s TEXT,h TEXT)');x.execute('CREATE TABLE IF NOT EXISTS activity(u TEXT,kind TEXT,value REAL,created TIMESTAMP DEFAULT CURRENT_TIMESTAMP)');return x
def hp(p,s):return hashlib.pbkdf2_hmac('sha256',p.encode(),bytes.fromhex(s),250000).hex()
def register(u,p):
 if len(u)<3 or len(p)<8:return False
 s=secrets.token_hex(16)
 try:
  with c() as x:x.execute('INSERT INTO users VALUES(?,?,?)',(u,s,hp(p,s)))
  return True
 except sqlite3.IntegrityError:return False
def login(u,p):
 with c() as x:r=x.execute('SELECT s,h FROM users WHERE u=?',(u,)).fetchone()
 return bool(r and secrets.compare_digest(hp(p,r[0]),r[1]))
def log(u,k,v):
 with c() as x:x.execute('INSERT INTO activity(u,kind,value) VALUES(?,?,?)',(u,k,v))
def history(u):
 with c() as x:return x.execute('SELECT kind,value,created FROM activity WHERE u=? ORDER BY created',(u,)).fetchall()
