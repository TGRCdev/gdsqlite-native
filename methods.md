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
If the path starts with "res://", it will use `open_buffered` implicitly.

### bool open_buffered(path: String, buffers: PoolByteArray, size: int)
Opens a temporary database with the data in `buffer`. Used for opening databases stored in res:// or compressed databases. Returns `true` if the database was opened successfully.
Can be written to, but the changes are NOT saved!

### bool query(statement: String)
Queries the database with the given SQL statement. Returns `true` if no errors occurred.

### bool query_all(statement: String)
Queries the database with a list of SQL statements, separated by semicolons. Returns `true` if no errors occurred.

### bool query_with_args(statement: String, args: Array)
Queries the database with the given SQL statement, replacing any `?` with arguments supplied by `args`. Returns `true` if no errors occurred.