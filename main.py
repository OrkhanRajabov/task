import pymysql
import requests
from datetime import datetime

def convert_date(date_str):
    try:
        date_obj = datetime.strptime(date_str, '%d %b %Y')
        return date_obj.strftime('%Y-%m-%d')
    except ValueError:
        return None


conn = pymysql.connect(
    host='127.0.0.1',
    user='root',
    password='12345',
    db='Task',
    port=3306,
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)

MOVIE = input("Enter the name of the film: ")

API_KEY = "5d9df2b8"


api_url = f'https://www.omdbapi.com/?t={MOVIE}&apikey={API_KEY}'



response = requests.get(api_url)
data = response.json()

if data.get('Response') == 'False':
    print("Movie not found.")
else:   
    Title = data.get('Title', '')
    Released = data.get('Released', '')
    Genre = data.get('Genre', '')
    Director = data.get('Director', '')

    
    Released = convert_date(Released)


    cursor = conn.cursor()
    cursor.execute('''INSERT INTO movie_info (title, released, genre, director) VALUES (%s, %s, %s, %s)''',
        (Title, Released, Genre, Director))

    
    conn.commit()


conn.close()