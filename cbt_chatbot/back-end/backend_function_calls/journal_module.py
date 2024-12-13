import sqlite3
from datetime import datetime

class JournalModule:
    def __init__(self, db_path):
        """
        Initialize the JournalModule with the path to the database.
        
        Args:
            db_path (str): The path to the SQLite database file.
        """
        self.db_path = db_path
        self._create_journal_table()

    def _create_journal_table(self):
        """
        Create the journal table if it doesn't exist.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS journal (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    entry TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def retrieve_journal_entries(self, user_id):
        """
        Retrieve journal entries for a specific user from the database.
        
        Args:
            user_id (int): The ID of the user.
        
        Returns:
            list: A list of journal entries.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT entry, timestamp FROM journal WHERE user_id = ?', (user_id,))
            entries = cursor.fetchall()
        return entries

    def add_journal_entry(self, user_id, entry):
        """
        Add a new journal entry to the database.
        
        Args:
            user_id (int): The ID of the user.
            entry (str): The journal entry text.
        
        Returns:
            str: Confirmation message.
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO journal (user_id, entry) VALUES (?, ?)', (user_id, entry))
            conn.commit()
        return "Journal entry added successfully."

# Example usage
if __name__ == "__main__":
    db_path = 'journal.db'
    journal_module = JournalModule(db_path)
    
    # Add a new journal entry
    user_id = 1
    entry = "Today I learned about ASGI and WSGI in Django."
    print(journal_module.add_journal_entry(user_id, entry))
    
    # Retrieve journal entries for the user
    entries = journal_module.retrieve_journal_entries(user_id)
    for entry, timestamp in entries:
        print(f"{timestamp}: {entry}")