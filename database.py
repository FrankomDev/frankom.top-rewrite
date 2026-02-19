import sqlite3

class Entry:
    def __init__(self, table_name : str, cells : str, cells_to_get : str):
        self.table = table_name
        self.get_cells = cells_to_get
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute(f"CREATE TABLE IF NOT EXISTS {self.table} (id int, {cells})")
        self.id = 0
        get_id = cursor.execute(f"SELECT id FROM {self.table} ORDER BY id DESC").fetchone()
        if get_id != None:
            self.id = int(get_id[0])
        connection.commit()
        connection.close()
    
    def get_data(self):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        data = cursor.execute(f"SELECT {self.get_cells} FROM {self.table} ORDER BY id DESC").fetchall()
        connection.close()
        return data

    def get_content_glob(self, id : int, cells : str):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        data = cursor.execute(f"SELECT {cells} FROM {self.table} WHERE id = {id}").fetchone()
        connection.close()
        return data

    def post_content_glob(self, cells : list):
        cells.insert(0, self.id+1)
        cells = tuple(cells)
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute(f"INSERT INTO {self.table} VALUES (?, ?, ?)", cells)
        self.id+=1
        connection.commit()
        connection.close() 

    def remove_content(self, id : int):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute(f"DELETE FROM {self.table} WHERE id = {id}")
        connection.commit()
        connection.close()
    
    def update_content(self, id: int, title : str, content : str):
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute(f"UPDATE {self.table} SET title = ?, content = ? WHERE id = {id}", (title, content))
        connection.commit()
        connection.close()


class Guestbook(Entry):
    def __init__(self):
        super().__init__(table_name="guestbook", cells="username text, message text", cells_to_get="username, message, id")
    def post_message(self, username : str, message : str):
        self.post_content_glob([username, message])

class Projects(Entry):
    def __init__(self):
        super().__init__(table_name="projects", cells="title text, content text", cells_to_get="title, id")
    def get_content(self, id):
        return self.get_content_glob(id, cells="title, content")
    def post_project(self, title : str, content : str):
        self.post_content_glob([title, content])

class Blog_posts(Entry):
    def __init__(self):
        super().__init__(table_name="blog", cells="title text, content text", cells_to_get="title, id")
    def get_content(self, id):
        return self.get_content_glob(id, cells="title, content")
    def post_blog(self, title : str, content : str):
        self.post_content_glob([title, content])