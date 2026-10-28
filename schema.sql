-- Fictional training data. Amounts are EUR; dates are ISO YYYY-MM-DD.
PRAGMA foreign_keys = ON;
CREATE TABLE clients (
    client_id INTEGER PRIMARY KEY,
    client_name TEXT NOT NULL UNIQUE,
    sector TEXT NOT NULL,
    region TEXT NOT NULL
);
CREATE TABLE projects (
    project_id INTEGER PRIMARY KEY,
    client_id INTEGER NOT NULL REFERENCES clients(client_id),
    project_type TEXT NOT NULL,
    start_date TEXT NOT NULL,
    planned_end_date TEXT NOT NULL,
    actual_end_date TEXT,
    status TEXT NOT NULL CHECK (status IN ('active', 'completed', 'cancelled')),
    budget INTEGER NOT NULL CHECK (budget > 0),
    CHECK (planned_end_date >= start_date),
    CHECK (actual_end_date IS NULL OR actual_end_date >= start_date),
    CHECK ((status = 'completed' AND actual_end_date IS NOT NULL)
        OR (status IN ('active', 'cancelled') AND actual_end_date IS NULL))
);
CREATE TABLE markets (
    market_id INTEGER PRIMARY KEY,
    market_name TEXT NOT NULL UNIQUE,
    region TEXT NOT NULL
);
CREATE TABLE project_markets (
    project_id INTEGER NOT NULL REFERENCES projects(project_id),
    market_id INTEGER NOT NULL REFERENCES markets(market_id),
    PRIMARY KEY (project_id, market_id)
);
CREATE TABLE invoices (
    invoice_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(project_id),
    invoice_date TEXT NOT NULL,
    amount INTEGER NOT NULL CHECK (amount > 0),
    paid_flag INTEGER NOT NULL CHECK (paid_flag IN (0, 1))
);
CREATE TABLE survey_waves (
    wave_id INTEGER PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(project_id),
    wave_number INTEGER NOT NULL CHECK (wave_number > 0),
    launch_date TEXT NOT NULL,
    close_date TEXT,
    completes_target INTEGER NOT NULL CHECK (completes_target > 0),
    completes_actual INTEGER NOT NULL CHECK (completes_actual >= 0),
    UNIQUE (project_id, wave_number),
    CHECK (close_date IS NULL OR close_date >= launch_date)
);
