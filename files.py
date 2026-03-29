import os
from werkzeug.utils import secure_filename

class Files:
    def __init__(self):
        self.directory = "static/uploads"

    def get(self) -> list:
        if os.path.exists(self.directory):
            return os.listdir(self.directory)
        else:
            os.mkdir(self.directory)
            return []
    
    def upload(self, file):
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(self.directory, filename))
    
    def delete(self, name):
        path = os.path.join(self.directory, name)
        if os.path.exists(path):
            os.remove(path)