extends Node

const SQLite = preload("res://lib/gdsqlite.gdns");

const db_path = "res://secret_info.db"
const password = "banana bread"

func _ready():
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
				printline += ' - "' + agent["nick_name"] + '"'
			print(printline)
	else:
		print("Failed to retrieve secret info!");
