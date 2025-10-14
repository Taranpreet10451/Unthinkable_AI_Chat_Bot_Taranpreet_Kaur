import sqlite3
import json
from config import DATABASE_PATH

def init_database():
    """
    Initialize the SQLite database with sessions table.
    Creates the database file and table if they don't exist.
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Create sessions table to store conversation history
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sessions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT UNIQUE NOT NULL,
            conversation_history TEXT DEFAULT '[]',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print(f"Database initialized at {DATABASE_PATH}")

def get_session_history(session_id):
    """
    Retrieve conversation history for a given session_id.
    
    Args:
        session_id (str): Unique session identifier
        
    Returns:
        list: List of conversation messages
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT conversation_history FROM sessions WHERE session_id = ?
    ''', (session_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if result:
        return json.loads(result[0])
    return []

def save_session_history(session_id, conversation_history):
    """
    Save conversation history for a session.
    
    Args:
        session_id (str): Unique session identifier
        conversation_history (list): List of conversation messages
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Convert conversation history to JSON string
    history_json = json.dumps(conversation_history)
    
    # Insert or update session
    cursor.execute('''
        INSERT OR REPLACE INTO sessions (session_id, conversation_history, updated_at)
        VALUES (?, ?, CURRENT_TIMESTAMP)
    ''', (session_id, history_json))
    
    conn.commit()
    conn.close()

def clear_session_history(session_id):
    """
    Clear conversation history for a session.
    
    Args:
        session_id (str): Unique session identifier
    """
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute('''
        DELETE FROM sessions WHERE session_id = ?
    ''', (session_id,))
    
    conn.commit()
    conn.close()
    print(f"Session {session_id} history cleared")
