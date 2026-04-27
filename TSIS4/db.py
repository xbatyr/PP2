from config import load_config

try:
    import psycopg2
except ModuleNotFoundError:
    psycopg2 = None

LAST_DB_ERROR = ""


SCHEMA = """
CREATE TABLE IF NOT EXISTS players (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS game_sessions (
    id SERIAL PRIMARY KEY,
    player_id INTEGER REFERENCES players(id),
    score INTEGER NOT NULL,
    level_reached INTEGER NOT NULL,
    played_at TIMESTAMP DEFAULT NOW()
);
"""


def connect():
    global LAST_DB_ERROR
    if not psycopg2:
        LAST_DB_ERROR = "psycopg2 is not installed"
        return None

    config = load_config()
    try:
        LAST_DB_ERROR = ""
        return psycopg2.connect(
            host=config.get("host", "localhost"),
            dbname=config.get("dbname") or config.get("database"),
            user=config.get("user", ""),
            password=config.get("password", ""),
            port=config.get("port", 5432),
        )
    except Exception as error:
        LAST_DB_ERROR = str(error)
        return None


def close_db(conn, cur=None):
    if cur:
        cur.close()
    if conn:
        conn.close()


def init_db():
    conn = connect()
    if not conn:
        return False
    cur = None
    try:
        cur = conn.cursor()
        cur.execute(SCHEMA)
        conn.commit()
        close_db(conn, cur)
        return True
    except Exception as error:
        global LAST_DB_ERROR
        LAST_DB_ERROR = str(error)
        close_db(conn, cur)
        return False


def get_player_id(cur, username):
    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    row = cur.fetchone()
    if row:
        return row[0]

    cur.execute("INSERT INTO players (username) VALUES (%s) RETURNING id", (username,))
    return cur.fetchone()[0]


def save_result(username, score, level):
    conn = connect()
    if not conn:
        return False
    cur = None
    try:
        cur = conn.cursor()
        player_id = get_player_id(cur, username or "Player")
        cur.execute(
            "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
            (player_id, int(score), int(level)),
        )
        conn.commit()
        close_db(conn, cur)
        return True
    except Exception as error:
        global LAST_DB_ERROR
        LAST_DB_ERROR = str(error)
        close_db(conn, cur)
        return False


def get_personal_best(username):
    if not username:
        return 0
    conn = connect()
    if not conn:
        return 0
    cur = None
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT MAX(game_sessions.score)
            FROM game_sessions
            JOIN players ON players.id = game_sessions.player_id
            WHERE players.username = %s
            """,
            (username,),
        )
        row = cur.fetchone()
        close_db(conn, cur)
        return row[0] or 0
    except Exception as error:
        global LAST_DB_ERROR
        LAST_DB_ERROR = str(error)
        close_db(conn, cur)
        return 0


def get_top_scores():
    conn = connect()
    if not conn:
        return []
    cur = None
    try:
        cur = conn.cursor()
        cur.execute(
            """
            SELECT players.username, game_sessions.score, game_sessions.level_reached, game_sessions.played_at
            FROM game_sessions
            JOIN players ON players.id = game_sessions.player_id
            ORDER BY game_sessions.score DESC, game_sessions.level_reached DESC, game_sessions.played_at DESC
            LIMIT 10
            """
        )
        rows = cur.fetchall()
        close_db(conn, cur)
        return rows
    except Exception as error:
        global LAST_DB_ERROR
        LAST_DB_ERROR = str(error)
        close_db(conn, cur)
        return []


def get_db_error():
    return LAST_DB_ERROR
