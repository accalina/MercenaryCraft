
import sqlite3
import bcrypt
import random

# CORE ---------------------------------------------------------------------------------------------
def query(sql, intent='get'):
	con = sqlite3.connect('merc.db')
	cursor = con.cursor()
	cursor.execute(sql)
	if intent != 'get':
		con.commit()
		return True
	else:
		return cursor.fetchall()


# AUTHENTICATION -----------------------------------------------------------------------------------
def register(username, password, mercname):
	password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
	result = query("INSERT INTO account (username, password, mercname, merccash) VALUES ('{}','{}','{}', 15)".format(username, password.decode('utf-8'), mercname),"post")
	return result

def login(username, password):
	password = password.encode()
	try:
		hashed = query(f"select password from account where username = '{username}'")[0][0].encode()
		if bcrypt.checkpw(password, hashed):
			return True
		else:
			return False
	except:
		return False


# PLAYER -------------------------------------------------------------------------------------------
def get_info_player(username):
	result = query(f"select username, mercname, merccash from account where username = '{username}'")[0]
	return result
	
# BUY and LIST HUNTERS -----------------------------------------------------------------------------
def myhunter(username):
	result = query(f"SELECT * FROM myhunters INNER JOIN hunters on myhunters.hunterid = hunters.id where myhunters.owner = '{username}'")
	return result

def hunterlist():
	result = query(f"SELECT * FROM hunters")
	return result

def buyhunter(hunterid, owner):
	hunterprice = query(f"SELECT price from hunters where id = '{hunterid}'")[0][0]
	mymoney = query(f"SELECT merccash from account where username = '{owner}'")[0][0]
	if int(hunterprice) <= int(mymoney):
		query("UPDATE account SET merccash='{}' WHERE username='{}'".format( int(mymoney) - int(hunterprice), owner ),"update")
		result = query(f"INSERT INTO myhunters (hunterid, owner) VALUES ('{hunterid}','{owner}')","insert")
		return True
	else:
		return False

# OPERATIONS and ENEMIES ---------------------------------------------------------------------------
def enemies():
	enemylist = query("SELECT * FROM enemies")
	return enemylist

def fight(enemy, hunter, username):
	cash = query(f"SELECT merccash FROM account where username = '{username}'")[0][0]
	h_id, h_name, h_hp, h_min, h_max = query(f"SELECT a.id, b.name, b.health, b.min, b.max FROM myhunters as a INNER JOIN hunters as b on a.hunterid = b.id where a.id = '{hunter}'")[0]
	e_id, e_name, e_hp, e_min, e_max, e_money = query(f"SELECT id, name, health, min, max, money from enemies where id = '{enemy}'")[0]

	report = []
	winner = ""
	battle = True

	while battle == True:
		h_atk = random.randint(h_min, h_max)
		e_hp  = e_hp - h_atk
		report.append(f"{h_name} Attack inflict {h_atk} damage, {e_name} have {e_hp} HP left")

		if e_hp <= 0:
			battle = False
			report.append("Battle is over")
			winner = f"Hunter {h_name}"
			wincash = e_money + cash
			query(f"update account set merccash = '{wincash}' where username = '{username}'","update")
			break

		e_atk = random.randint(e_min, e_max)
		h_hp = h_hp - e_atk
		report.append(f"{e_name} Attack inflict {e_atk} damage, {h_name}'s have {h_hp} left")

		if h_hp <= 0:
			battle = False
			report.append("Battle is over")
			winner = f"Enemy {e_name}"
			break

	return report, winner
