import sqlite3
import logging

class Database:
    def __init__(self, db_name='applications.db'):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        """Инициализирует базу данных"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                username TEXT,
                departure_city TEXT,
                destination TEXT,
                dates TEXT,
                nights TEXT,
                travelers TEXT,
                hotel_class TEXT,
                meals TEXT,
                wishes TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
        logging.info("База данных инициализирована")
    
    def save_application(self, application_data):
        """Сохраняет заявку в базу данных"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO applications 
            (user_id, username, departure_city, destination, dates, nights, travelers, hotel_class, meals, wishes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            application_data['user_id'],
            application_data['username'],
            application_data['departure_city'],
            application_data['destination'],
            application_data['dates'],
            application_data['nights'],
            application_data['travelers'],
            application_data['hotel_class'],
            application_data['meals'],
            application_data['wishes']
        ))
        conn.commit()
        conn.close()
        logging.info(f"Заявка от пользователя {application_data['username']} сохранена в базу данных")
        
    def get_applications(self):
        """Получить все заявки (для админки)"""
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM applications ORDER BY created_at DESC')
        applications = cursor.fetchall()
        conn.close()
        return applications


def get_application_count(self):
    """Получить количество заявок"""
    conn = sqlite3.connect(self.db_name)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM applications')
    count = cursor.fetchone()[0]
    conn.close()
    return count