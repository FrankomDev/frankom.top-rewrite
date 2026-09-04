import os

from sqlalchemy import Engine, Text
from sqlmodel import Field, SQLModel, Session, create_engine, select

class Database:

    class Guestbook:
        class GuestbookDb(SQLModel, table=True):
            id : int | None = Field(default=None, primary_key=True)
            username : str
            message : str

        def __init__(self, session : Session) -> None:
            self.session = session

        def post(self, username : str, message : str) -> None:
            entry = self.GuestbookDb(username=username, message=message)
            self.session.add(entry)
            self.session.commit()
            self.session.refresh(entry)

        def get(self):
            data = self.session.exec(select(self.GuestbookDb).order_by(self.GuestbookDb.id.desc())).all()
            #print(data)
            return data

        def delete(self, id : int) -> bool:
            cmd = select(self.GuestbookDb).where(self.GuestbookDb.id == id);
            entry = self.session.exec(cmd).first()
            if entry is None:
                return False
            else:
                self.session.delete(entry)
                self.session.commit()
                return True

    class Blog:
        class BlogDb(SQLModel, table=True):
            id : int | None = Field(default=None, primary_key=True)
            title : str
            content : str = Field(sa_type=Text)

        def __init__(self, session : Session) -> None:
            self.session = session

        def post(self, title : str, content : str) -> None:
            entry = self.BlogDb(title=title, content=content)
            self.session.add(entry)
            self.session.commit()
            self.session.refresh(entry)

        def get(self):
            cmd = select(self.BlogDb.id, self.BlogDb.title).order_by(self.BlogDb.id.desc())
            data = self.session.exec(cmd).all()
            items = []
            for i in data:
                items.append({"id": i[0], "title": i[1]})
            return items

        def get_by_id(self, id : int):
            cmd = select(self.BlogDb.title, self.BlogDb.content).where(self.BlogDb.id == id)
            data = self.session.exec(cmd).first()
            if data is not None:
                return {"title": data[0], "content": data[1]}
            return []

        def delete(self, id : int) -> bool:
            cmd = select(self.BlogDb).where(self.BlogDb.id == id);
            entry = self.session.exec(cmd).first()
            if entry is None:
                return False
            else:
                self.session.delete(entry)
                self.session.commit()
                return True

        def update(self, id : int, title : str, content : str) -> bool:
            cmd = select(self.BlogDb).where(self.BlogDb.id == id);
            entry = self.session.exec(cmd).first()
            if entry is None:
                return False
            else:
                entry.title = title;
                entry.content = content;
                self.session.add(entry)
                self.session.commit()
                self.session.refresh(entry)
                return True

    class Projects:
        class ProjectsDb(SQLModel, table=True):
            id : int | None = Field(default=None, primary_key=True)
            title : str
            content : str = Field(sa_type=Text)

        def __init__(self, session : Session) -> None:
            self.session = session

        def post(self, title : str, content : str) -> None:
            entry = self.ProjectsDb(title=title, content=content)
            self.session.add(entry)
            self.session.commit()
            self.session.refresh(entry)

        def get(self):
            cmd = select(self.ProjectsDb.id, self.ProjectsDb.title).order_by(self.ProjectsDb.id.desc())
            data = self.session.exec(cmd).all()
            items = []
            for i in data:
                items.append({"id": i[0], "title": i[1]})
            return items

        def get_by_id(self, id : int):
            cmd = select(self.ProjectsDb.title, self.ProjectsDb.content).where(self.ProjectsDb.id == id)
            data = self.session.exec(cmd).first()
            if data is not None:
                return {"title": data[0], "content": data[1]}
            return []

        def delete(self, id : int) -> bool:
            cmd = select(self.ProjectsDb).where(self.ProjectsDb.id == id);
            entry = self.session.exec(cmd).first()
            if entry is None:
                return False
            else:
                self.session.delete(entry)
                self.session.commit()
                return True

        def update(self, id : int, title : str, content : str) -> bool:
            cmd = select(self.ProjectsDb).where(self.ProjectsDb.id == id);
            entry = self.session.exec(cmd).first()
            if entry is None:
                return False
            else:
                entry.title = title;
                entry.content = content;
                self.session.add(entry)
                self.session.commit()
                self.session.refresh(entry)
                return True


    def __init__(self) -> None:
        password = os.getenv("PASSWORD")
        db = os.getenv("DATABASE")
        self.engine : Engine = create_engine(f"mysql://root:{password}@{db}/frankomtop")
        SQLModel.metadata.create_all(self.engine)
        self.session : Session = Session(self.engine)

        self.guestbook = self.Guestbook(self.session)
        self.blog = self.Blog(self.session)
        self.projects = self.Projects(self.session)
