# SQLite
*extends Reference*

A wrapper class that lets you perform SQL statements on an SQLite database file.
For queries that involve arbitrary user input, you should use methods that end in `*_with_args`, as these protect against SQL injection.

## Methods

### void close()
Closes the database handle.

### Array fetch_array(statement: String)
Returns the result of `statement` as an `Array` of rows.
Each row is a `Dictionary`, and each column can be accessed with either its name or its column position.

### Array fetch_array_with_args(statement: String, args: Array)
Returns the result of `statement` as an `Array` of rows, substituting each `?` using `args`.
Each row is a `Dictionary`, and each column can be accessed with either its name or its column position.

### Array fetch_assoc(statement: String)
Returns the result of `statement` as an `Array` of rows.
Each row is a `Dictionary`, and the keys are the names of the columns.

### Array fetch_assoc_with_args(statement: String, args: Array)
Returns the result of `statement` as an `Array` of rows, substituting each `?` with `args`.
Each row is a `Dictionary`, and the keys are the names of the columns.

### bool open(path: String)
Opens the database file at the given path. Returns `true` if the database was successfully opened, `false` otherwise.
If the path starts with "res://" and the script is ran outside of the editor, `open_buffered` will be used implicitly.

### bool open_buffered(name: String, buffers: PoolByteArray, size: int)
Opens a temporary database with the data in `buffer`. Used for opening databases stored in res:// or compressed databases. Returns `true` if the database was opened successfully.
Can be written to, but the changes are NOT saved!

### bool open_buffered_with_flags(name: String, buffers: PoolByteArray, size: int)
Opens a temporary database with the data in `buffer` with the given flags. Used for opening databases stored in res:// or compressed databases. Returns `true` if the database was opened successfully.
Can be written to, but the changes are NOT saved!

The accepted flags are available as constants in `res://lib/gdsqlite/flags.gd`.

### bool open_encrypted(path: String, password: String)
Opens the database file at the given path with the given password. Returns `true` if the database was successfully opened and decrypted, `false` otherwise.
If the path starts with "res://" and the script is ran outside of the editor, `open_buffered` will be used implicitly before decrypting.

### bool open_encrypted_with_flags(path: String, password: String, flags: int)
Opens the database file at the given path with the given password using the given SQLITE_OPEN flags. Returns `true` if the database was successfully opened and decrypted, `false` otherwise.
If the path starts with "res://" and the script is ran outside of the editor, `open_buffered_with_flags` will be used implicitly before decrypting.

The accepted flags are available as constants in `res://lib/gdsqlite/flags.gd`.

### bool open_with_flags(path: String, password: String, flags: int)
Opens the database file at the given path with the given flags. Returns `true` if the database was successfully opened, `false` otherwise.
If the path starts with "res://" and the script is ran outside of the editor, `open_buffered_with_flags` will be used implicitly.

The accepted flags are available as constants in `res://lib/gdsqlite/flags.gd`.

### bool query(statement: String)
Queries the database with the given SQL statement. Returns `true` if no errors occurred.

### bool query_all(statement: String)
Queries the database with a list of SQL statements, separated by semicolons. Returns `true` if no errors occurred.

### bool query_with_args(statement: String, args: Array)
Queries the database with the given SQL statement, replacing any `?` with arguments supplied by `args`. Returns `true` if no errors occurred.