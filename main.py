from flask import Flask, render_template, request
from sqlalchemy import *
import sqlalchemy.orm
from sqlalchemy.orm import sessionmaker, relationship

app = Flask(__name__)

# Create a SQLite database engine
engine = create_engine('sqlite:///database.db')

Base = sqlalchemy.orm.declarative_base()


class Pupil(Base):
    __tablename__ = 'pupils'
    id = Column(Integer, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name


class Course(Base):
    __tablename__ = 'courses'
    id = Column(Integer, primary_key=True)
    pupil_id = Column(Integer, ForeignKey('pupils.id'))
    name = Column(String)
    pupil = relationship('Pupil', backref='courses')

    def __init__(self, name, pupil):
        self.name = name
        self.pupil = pupil


# Drop existing tables
# Base.metadata.drop_all(engine)

# Create Database
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


@app.route('/', methods=['GET', 'POST'])
def add_pupil():
    if request.method == 'POST':
        name = request.form['name']
        course_name = request.form['course_name']

        new_pupil = Pupil(name=name)
        session.add(new_pupil)

        new_course = Course(name=course_name, pupil=new_pupil)
        session.add(new_course)

        session.commit()

    pupils = session.query(Pupil).all()

    return render_template('index.html', pupils=pupils)


if __name__ == '__main__':
    app.run(debug=True)
