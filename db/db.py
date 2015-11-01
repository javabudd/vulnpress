from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, ForeignKey, Text, Boolean
from db.exploit import Exploit
from db.exploit_type import ExploitType
from db.random_quote import RandomQuote
import json
import random

class Db:
    # Create a single exploit
    def create_exploit(self, type_id: int, name: str, version: str, exploit_body: str, exploit_headers: dict, url: str):
        session = self.get_session()
        session.add(Exploit(type_id=type_id, name=name, version=version, exploit_body=exploit_body,
                            exploit_headers=json.dumps(exploit_headers), url=url))
        session.commit()

    # Create a single exploit type
    def create_exploit_type(self, name: str):
        session = self.get_session()
        session.add(ExploitType(name=name))
        session.commit()

    # Get all exploits
    def get_exploits(self):
        return self.get_session().query(Exploit).order_by(Exploit.name).all()

    # Get all exploit types
    def get_exploit_types(self):
        return self.get_session().query(ExploitType).all()

    # Get exploits by exploit type
    def get_exploits_by_exploit_type_id(self, exploit_type_id: int):
        return self.get_session().query(Exploit).join(ExploitType).filter(ExploitType.id == exploit_type_id).all()

    # Get exploits by exploit type short name
    def get_exploits_by_exploit_type_short_name(self, short_name: str):
        return self.get_session().query(Exploit).join(ExploitType).filter(ExploitType.short_name == short_name).all()

    # Get a single exploit by an ID
    def get_exploit_by_id(self, exploit_id: int):
        return self.get_session().query(Exploit).filter(Exploit.id == exploit_id).one()

    # Get a single exploit by a name
    def get_exploit_by_name(self, exploit_name: str):
        return self.get_session().query(Exploit).filter(Exploit.name == exploit_name).one()

    # Get a single exploit type by an ID
    def get_exploit_type_by_id(self, exploit_id: int):
        return self.get_session().query(ExploitType).filter(ExploitType.id == exploit_id).one()

    # Get a single exploit type by a name
    def get_exploit_type_by_name(self, exploit_type: str):
        return self.get_session().query(ExploitType).filter(ExploitType.name == exploit_type).one()

    # Get a random quote
    def get_random_quote(self):
        return random.choice(self.get_session().query(RandomQuote).all()).quote

    # Delete an exploit type
    def delete_exploit_type(self, type_id: int):
        session = self.get_session()

        session.query(ExploitType.id).filter_by(id=type_id).delete()
        session.commit()

    # Create base tables
    def create_base_tables(self):
        metadata = MetaData(bind=self.create_engine())

        Table('random_quote', metadata,
              Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
              Column('quote', Text, nullable=False)
              )
        Table('exploit_type', metadata,
              Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
              Column('name', String(128), nullable=False),
              Column('short_name', String(32), nullable=False)
              )
        Table('exploit', metadata,
              Column('id', Integer, primary_key=True, nullable=False, autoincrement=True),
              Column('type_id', Integer, ForeignKey(ExploitType.id), nullable=False),
              Column('validator_id', Integer, nullable=False),
              Column('name', String(128), nullable=False),
              Column('version', String(64), nullable=False),
              Column('url', String(128), nullable=False),
              Column('request_method', String(12), nullable=False, default='GET'),
              Column('exploit_url', String(128), nullable=False),
              Column('exploit_body', Text, nullable=True),
              Column('exploit_headers', Text, nullable=True),
              Column('is_url_encode', Boolean, nullable=False, default=False),
              Column('is_authenticated', Boolean, nullable=False, default=False)
              )

        metadata.create_all(checkfirst=True)

    # Get the default session
    def get_session(self):
        session = sessionmaker()
        session.configure(bind=self.create_engine())

        return session()

    @staticmethod
    # Create the default engine
    def create_engine():
        return create_engine('sqlite:///db/exploits.db', echo=False)
