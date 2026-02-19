import sqlite3

def initialize_db():
    conn = sqlite3.connect('ri_os_memory.db')
    cursor = conn.cursor()
    
    # Create the table for communications and bias tracking
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS imperial_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            sender_id TEXT,
            original_text TEXT,
            translated_text TEXT,
            bias_score REAL DEFAULT 0.0,
            metadata TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    print("🏛️ RI-OS: Sacred Corpus initialized. Memory is now active.")

if __name__ == "__main__":
    initialize_db()
