from database import create_connection


class MasterData:

    def add_master(master_id, master_name, master_phone):
        cnx, cur = create_connection()
        cur.execute(f'''INSERT INTO masters(`master_id`,`master_name`,`master_phone`)
                        VALUES ({master_id},"{master_name}","{master_phone}") ''')
        cnx.commit()

    def update_master(master_id, master_name, master_phone):
        cnx, cur = create_connection()
        cur.execute(
            f'''UPDATE masters SET `master_name`="{master_name}", `master_phone`="{master_phone}"
                        WHERE `master_id`={master_id} ''')
        cnx.commit()

    def get_master(master_id):
        cnx, cur = create_connection()
        cur.execute(
            f''' SELECT * FROM `masters` WHERE `master_id` = {master_id}''')
        master = cur.fetchone()
        return master

    def update_master_point(master_id):
        cnx, cur = create_connection()
        cur.execute(
            f'''UPDATE masters SET `master_point` = `master_point` + 1 WHERE `master_id` = {master_id} ''')
        cnx.commit()

    def minus_master_point(master_number, points):
        cnx, cur = create_connection()
        cur.execute(
            f'''UPDATE masters SET `master_point` = `master_point` - {points} WHERE `master_phone` = {master_number} ''')
        cnx.commit()


class AdminData:
    def get_master_data():
        cnx, cur = create_connection()
        cur.execute(f'''SELECT * FROM masters''')
        master = cur.fetchall()
        return master

    def get_excel():
        cnx, cur = create_connection()
        cur.execute(
            f'''SELECT `master_name`, `master_phone`, `master_point` FROM masters''')
        master = cur.fetchall()
        return master
