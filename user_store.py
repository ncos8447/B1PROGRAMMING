import sqlite3

class UserStore:
    def __init__(self, db_path):
        # save database path
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        # create users table if it doesn't exist
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """)

        conn.commit()
        conn.close()

    def load(self):
        # return all users as list of dictionaries
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT id, name, email FROM users")
        rows = cursor.fetchall()

        conn.close()

        users = []
        for row in rows:
            users.append({
                "id": row[0],
                "name": row[1],
                "email": row[2]
            })

        return users

    def save(self, user_data):
        # insert new user into database
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO users (name, email) VALUES (?, ?)",
            (user_data["name"], user_data["email"])
        )

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return new_id

    def find_by_id(self, user_id):
        # find user by id
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, name, email FROM users WHERE id = ?",
            (user_id,)
        )

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "id": row[0],
                "name": row[1],
                "email": row[2]
            }

        return None

    def update_user(self, user_id, updated_data):
        # update user using sql update
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            (updated_data["name"], updated_data["email"], user_id)
        )

        conn.commit()
        success = cursor.rowcount > 0
        conn.close()

        return success

    def delete_user(self, user_id):
        # delete user using sql delete
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM users WHERE id = ?",
            (user_id,)
        )

        conn.commit()
        success = cursor.rowcount > 0
        conn.close()

        return success