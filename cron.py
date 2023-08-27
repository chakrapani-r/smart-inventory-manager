import psycopg2
import time

conn = None
cursor = None
try:
    conn = psycopg2.connect(host = 'localhost', dbname = 'inventory-manager', user = 'postgres', password = 'Exercise@2022', port = 5432)

    cursor = conn.cursor()

    while True:
        script = 'select count(*) as count from inventory'
        cursor.execute(script)
        record = cursor.fetchone()
        timestamp = time.time()
        print(f"{record[0]}, {timestamp}")
        with open('inventory_count.txt', 'a') as f:
            f.write(f"{record[0]}, {timestamp}\n")
        time.sleep(60)

    conn.commit()
except Exception as error:
    print(error)
finally:
    if cursor is not None:
        cursor.close()
    if conn is not None:
        conn.close()


