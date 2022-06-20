from database import mydb, cursor


class MasterData:

    def add_master(master_id, master_name, master_phone):
        cursor.execute(f'''INSERT INTO masters(`master_id`,`master_name`,`master_phone`)
                        VALUES ({master_id},"{master_name}","{master_phone}") ''')
        mydb.commit()

    def update_master(master_id, master_name, master_phone):
        cursor.execute(
            f'''UPDATE masters SET `master_name`="{master_name}", `master_phone`="{master_phone}"
                        WHERE `master_id`={master_id} ''')
        mydb.commit()

    def get_master(master_id):
        cursor.execute(f''' SELECT * FROM `masters` WHERE `master_id` = {master_id}''')
        master = cursor.fetchone()
        return master

    def update_master_point(master_id):
        cursor.execute(f'''UPDATE masters SET `master_point` = `master_point` + 1 WHERE `master_id` = {master_id} ''')
        mydb.commit()

    def minus_master_point(master_number, points):
        cursor.execute(
            f'''UPDATE masters SET `master_point` = `master_point` - {points} WHERE `master_phone` = {master_number} ''')
        mydb.commit()


class AdminData:

    
    def get_master_data():
        cursor.execute(f'''SELECT * FROM masters''')
        master = cursor.fetchall()
        return master

    def get_excel():
        cursor.execute(f'''SELECT `master_name`, `master_phone`, `master_point` FROM masters''')
        master = cursor.fetchall()
        return master
        
