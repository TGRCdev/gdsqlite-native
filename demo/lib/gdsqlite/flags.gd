extends Reference

# Flags accepted by SQLite.open_with_flags
# Any flags not included here are ignored

# More info on these flags: https://www.sqlite.org/c3ref/open.html

const SQLITE_OPEN_READONLY     = 0x00000001;
const SQLITE_OPEN_READWRITE    = 0x00000002;
const SQLITE_OPEN_CREATE       = 0x00000004;
const SQLITE_OPEN_URI          = 0x00000040;
const SQLITE_OPEN_MEMORY       = 0x00000080;
const SQLITE_OPEN_NOMUTEX      = 0x00008000;
const SQLITE_OPEN_FULLMUTEX    = 0x00010000;
const SQLITE_OPEN_SHAREDCACHE  = 0x00040000;
const SQLITE_OPEN_PRIVATECACHE = 0x00040000;
const SQLITE_OPEN_NOFOLLOW     = 0x01000000;

# Default flag values used by SQLite.open
const SQLITE_OPEN_DEFAULT = SQLITE_OPEN_READWRITE | SQLITE_OPEN_CREATE;
