CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    username TEXT NOT NULL COLLATE NOCASE,
    password TEXT NOT NULL COLLATE NOCASE,
    role TEXT CHECK(role IN ('admin', 'accountant', 'operator')),
    userid INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS companies (
    company_id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT NOT NULL COLLATE NOCASE,
    address TEXT NOT NULL COLLATE NOCASE,
    city TEXT NOT NULL COLLATE NOCASE,
    pincode TEXT NOT NULL,`
    mobile TEXT NOT NULL,
    email TEXT NOT NULL,
    fy_start_month TEXT,
    fy_start_year TEXT,
    fy_end_month TEXT,
    fy_end_year TEXT
);

CREATE TABLE IF NOT EXISTS customers ( 
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL COLLATE NOCASE
);
CREATE TABLE IF NOT EXISTS suppliers ( 
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL COLLATE NOCASE
);
CREATE TABLE IF NOT EXISTS items ( 
    id   INTEGER PRIMARY KEY,
    name TEXT NOT NULL COLLATE NOCASE
);