import mysql.connector

try:
    cnx = mysql.connector.connect(user="root", password="",host="localhost",database="db")
    cursor = cnx.cursor()
    
    create_table_querry = """
    CREATE TABLE IF NOT EXISTS bancodados(
            id INT AUTO_INCREMENT PRIMARY KEY,
            equipment_id VARCHAR(50) UNIQUE,
            timestamp DATETIME NOT NULL,
            value DECIMAL(10,2) NOT NULL
        )"""
    cursor.execute(create_table_querry)
    cnx.commit()

    show_tables_query = "SHOW TABLES"
    cursor.execute(show_tables_query)

    tables = cursor.fetchall()

    tables_exists = False
    for table in tables:
        if 'bancodados' in table:
            tables_exists = True
            break
    if tables_exists:
        print("A tabela bancodados foi encontrada")
    else:
        print("A tabela bancodados não foi encontrada")

    cursor.close()
    cnx.close()
except mysql.connector.Error as err:
    print("Erro: ", err)