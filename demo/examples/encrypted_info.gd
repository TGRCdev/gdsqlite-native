extends Node

const SQLite = preload("res://lib/gdsqlite.gdns");

const db_path = "user://secret_info.db"
const password = "banana bread"

func _ready():
	var file = File.new();
	if not file.file_exists(db_path):
		create_database();
	else:
		read_database();

func read_database():
	print("Reading database with secret info");
	var db = SQLite.new();
	if not db.open_encrypted(db_path, password):
		print("Couldn't open secret database!");
		return;
	
	var secret_info = db.fetch_assoc_with_args("SELECT * FROM agents");
	
	if not secret_info.empty():
		print("Retrieved secret info");
		for agent in secret_info:
			var printline = "Agent %d: %s %s" % [agent["id"], agent["first_name"], agent["last_name"]]
			if agent["nick_name"] != null:
				printline += " - " + agent["nick_name"]
			print(printline)
	else:
		print("Failed to retrieve secret info!");

func create_database():
	print("Creating database with secret info");
	var db = SQLite.new();
	if not db.open_encrypted(db_path, password):
		print("Couldn't create secret database!")
		return;
	
	db.query("""
	CREATE TABLE agents (
		id INTEGER PRIMARY KEY,
		first_name TEXT NOT NULL,
		last_name TEXT NOT NULL,
		nick_name TEXT
	)
	""")
	
	var secret_info = [
		["Juni", "Cortez", null],
		["Carmen", "Cortez", null],
		["Isador", "Cortez", "Machete"],
		["Donnagon", "Giggles", null],
		["Gerti", "Giggles", null]
	]
	
	for agent in secret_info:
		db.query_with_args("INSERT INTO agents (first_name, last_name, nick_name) VALUES (?,?,?)", agent);
	
	print("Secret database created at " + db_path);
