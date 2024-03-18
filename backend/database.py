from models import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime
from sqlalchemy import ForeignKey




Base = declarative_base()

engine = create_engine('sqlite:///../data.db')
Session = sessionmaker(bind=engine)

class Person(Base):
    __tablename__ = 'person'
    email = Column(String, primary_key=True)
    def __repr__(self):
        return f"user('{self.email}')"

class User(Base):
    __tablename__ = 'usr'
    person  = Column(String, ForeignKey('person.email'),nullable=False)
    id = Column(Integer, primary_key=True, autoincrement=True)
    host_code = Column(String, nullable=False)
    post = Column(String(50), nullable=False)
    auto_reply_switch = Column(Boolean, nullable=False, default=True)
    attendance = Column(Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"user('{self.host_code}', '{self.post}')"



class Sw(Base):
    __tablename__ = 'sw'
    id = Column(Integer, primary_key=True, autoincrement=True)
    host_code = Column(String)
    host_name = Column(String, nullable=False)
    switch = Column(Boolean, nullable=False, default=True)
    link = Column(Text, nullable=False)
    orgn = Column(String, nullable=False)

    def __repr__(self):
        return f"user('{self.host_code}','{self.link}','{self.orgn}')"

class certificate(Base):
    __tablename__ = 'certificate'

    id = Column(Integer, primary_key=True, autoincrement=True)  # Add this line
    sw_id = Column(String, ForeignKey('sw.host_code'), nullable=False)
    certificate_win = Column(Text, nullable=True)
    certificate_part = Column(Text, nullable=True)

    def __repr__(self):
        return f"user('{self.certificate_win}','{self.certificate_part}')"
class design(Base):
    __tablename__ = 'design'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Add this line
    sw_id = Column(String, ForeignKey('sw.host_code'), nullable=False)
    certificate_win = Column(Text, nullable=True)
    certificate_part = Column(Text, nullable=True)
    def __repr__(self):
        return f"user('{self.host_code}','{self.link}','{self.orgn}')"

class points(Base):
    __tablename__ = 'points'
    id = Column(Integer, primary_key=True, autoincrement=True)  # Add this line
    sw_id = Column(String, ForeignKey('sw.host_code'), nullable=False)
    person = Column(String, ForeignKey('person.email'), nullable=False)
    points = Column(Integer, nullable=False, default=0)
    




class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True, autoincrement=True)
    host_code = Column(String, nullable=False)
    to = Column(String(50), nullable=False)
    from_c = Column(String(50), nullable=False)
    viaeb = Column(String(10), nullable=False)
    message = Column(Text, nullable=False)
    timestamp = Column(String, nullable=False)
    point = Column(String, nullable=False, default='General')
    replyid = Column(String, nullable=False)
    proccessed_text = Column(Text, default='Waiting for Response...')

    def __repr__(self):
        return f"user('{self.host_code}','{self.timestamp}','{self.to}', '{self.from_c}', '{self.viaeb}', '{self.message}', '{self.replyid}')"



def message_adder_dab(host_id, to_c, from_country, viaeb_c, message_c, replyid_c, chit_pnt='General'):
    msg = Message(host_code=host_id, to=to_c, timestamp=datetime.now(), from_c=from_country, viaeb=viaeb_c, message=message_c, point=chit_pnt, replyid=replyid_c)
    Session.add(msg)
    Session.commit()

def swit(host_id):
    try:
        return Session.query(Sw).filter_by(host_code=host_id).first().switch
    except NoResultFound:
        return False

def change_switch(host_id):
    try:
        sw = Session.query(Sw).filter_by(host_code=host_id).first()
        sw.switch = not sw.switch
        Session.commit()
    except NoResultFound:
        pass

def change_switch_auto_r(user_idq):
    try:
        user = Session.query(User).filter_by(user_id=user_idq).first()
        user.auto_reply_switch = not user.auto_reply_switch
        Session.commit()
    except NoResultFound:
        pass

def message_to_list(query_result):
    msg_lst = []
    for i in query_result:
        try:
            t_m = [i.id, i.to, i.from_c, i.viaeb, i.message, i.timestamp, i.point, i.replyid, i.proccessed_text]
            msg_lst.append(t_m)
        except:
            pass
    return msg_lst

def msg_sent(host_id, admin_country):
    temp_msg = message_to_list(Session.query(Message).filter_by(host_code=host_id , from_c=admin_country).all())
    fnl = []
    for p in temp_msg:
        try:
            if p[-1].isnumeric():
                reply = Session.query(Message).filter_by(id=int(p[-1])).first().message
                p.pop()
                p.append(reply)
                fnl.append(p)
            else:
                fnl.append(p)
        except:
            pass
    return fnl




Base.metadata.create_all(engine)


# Create a new session
session = Session()


def add_email(email):
    person = Person(email=email)
    session.add(person)
    session.commit()


# add_email("harshdipashah@gmail.com")
# Create a new instance of the Sw class
sw = Sw(
    host_code='test_host_code',
    host_name='test_host_name',
    switch=True,
    link='http://example.com',
    orgn='test_orgn'
)

sw1 = Sw(
    host_code='test_host_code1',
    host_name='test_host_name1',
    switch=True,
    link='http://example1.com',
    orgn='test_orgn1'
)

sw2 = Sw(
    host_code='test_host_code2',
    host_name='test_host_name2',
    switch=False,
    link='http://example2.com',
    orgn='test_orgn2'
)

sw3 = Sw(
    host_code='test_host_code3',
    host_name='test_host_name3',
    switch=True,
    link='http://example3.com',
    orgn='test_orgn3'
)


# Add the new instance to the session
# session.add(sw)
# session.add(sw1)
# session.add(sw2)
# session.add(sw3)

# # Commit the session to write the changes to the database
# session.commit()


person  = session.query(Person).filter_by(email='harshdipashah@gmail.com').first()

user1 = User(
    person=person.email,
    host_code='test_host_code',
    post='test_post',
    auto_reply_switch=True,
    attendance=False
)

user2 = User(
    person=person.email,
    host_code='test_host_code2',
    post='test_post2',
    auto_reply_switch=False,
    attendance=True
)

# session.add(user1)
# session.add(user2)

# session.commit()