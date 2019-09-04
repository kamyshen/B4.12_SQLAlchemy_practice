import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DB_PATH = "sqlite:///sochi_athletes.sqlite3"
Base = declarative_base()

def connect_db():

    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)

    return session()

class User(Base):

    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    
class Athlete(Base):
    
    __tablename__ = "athelete"
    
    id = sa.Column(sa.Integer, primary_key=True)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.Text)
    
def find(id, session):
    query = session.query(User).filter(User.id == id)
    result = query.first()
    return result
    
def search_athlete(result, session, param, mode):
    athlets = session.query(Athlete).all()
    athlete_diff = {}
    if param == "age":
        user_birthdate = str_to_date(result.birthdate)
        for a in athlets:
            athlete_diff[a.name] = abs(str_to_date(a.birthdate) - user_birthdate)
        dif0 = datetime.timedelta(days=100000)
        matched = search_engine(athlete_diff, dif0)
        
        if mode == 1:
            if len(matched) == 1:
                return f"Ближайший атлет по возрасту - {matched[0]}"
            else:
                m = ", ".join(matched)
                return f"Ближайшие атлеты по возрасту: {m}"
        elif mode == 2:
            return f"Ближайший атлет по возрасту - {matched[0]}"
         
    elif param == "height":
        for a in athlets:
            if a.height == None:
                continue
            athlete_diff[a.name] = abs(float(a.height) - result.height)
        dif0 = 10
        matched = search_engine(athlete_diff, dif0)
        
        if mode == 1:
            if len(matched) == 1:
                return f"Ближайший атлет по росту - {matched[0]}"
            else:
                m = ", ".join(matched)
                return f"Ближайшие атлеты по росту: {m}"
        elif mode == 2:
            return f"Ближайший атлет по росту - {matched[0]}"
      
def search_engine(athlete_diff, dif0):
    for a, dif in athlete_diff.items():
        if dif < dif0:
            dif0 = dif
            matched = []
            matched.append(a)
        elif dif == dif0:
            matched.append(a)
    return matched
    
def str_to_date(string):
    return datetime.date(*[int(d) for d in (string.split("-"))])

def main():

    session = connect_db()
    id = input("Введи id ")
    mode = int(input("В случае, если поиск выдаст больше одного атлета,\nхотите увидеть их всех (введите 1)\nили первого найденного (введите 2) "))
    result = find(id, session)
    if result:
        print(search_athlete(result, session, "age", mode))
        print(search_athlete(result, session, "height",mode))
    else:
        print("Пользователь с таким id в базе не найден")
    
if __name__ == "__main__":
    main()