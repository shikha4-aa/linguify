import mysql.connector

def insert_image(word_id, language_id, session_number, word, image_path):
    conn = mysql.connector.connect(host='localhost', user='root', password='Vinayak@23', database='Linguify')
    cursor = conn.cursor()

    with open(image_path, 'rb') as file:
        binary_data = file.read()
        sql = "INSERT INTO images (word_id, language_id, session_number, word, image) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (word_id, language_id, session_number, word, binary_data))
        conn.commit()

    cursor.close()
    conn.close()

# Usage
insert_image(10, 4, 1, 'HOME', 'images/teaching/home.jpeg')
