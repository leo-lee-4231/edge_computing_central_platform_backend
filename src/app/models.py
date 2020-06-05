# -*- encoding: utf-8 -*-
#
# data models for app
#
# 20-3-30 leo : Init

from datetime import datetime
from . import db


class Book:
    def __init__(self, name, ISBN, author, ID=None):
        self.id = ID
        self.name = name
        self.ISBN = ISBN
        self.author = author

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'ISBN': self.ISBN,
            'author': self.author
        }

    def save(self):
        try:
            with db.connector.cursor() as cursor:
                sql = "INSERT INTO books(name, ISBN, author) " \
                      "VALUES ('%s', '%s', '%s') " \
                      % (self.name, self.ISBN, self.author)
                cursor.execute(sql)
                self.id = cursor.lastrowid
                db.connector.commit()
        except Exception as err:
            db.connector.rollback()
            print('error in save book')
            print(str(err))

    def update(self):
        try:
            with db.connector.cursor() as cursor:
                sql = "UPDATE books SET name = '%s', ISBN = '%s'," \
                      " author = '%s' WHERE id = %s" \
                      % (self.name, self.ISBN, self.author, self.id)
                cursor.execute(sql)
                db.connector.commit()
        except Exception as err:
            db.connector.rollback()
            print('error in update book')
            print(str(err))

    def delete(self):
        try:
            with db.connector.cursor() as cursor:
                sql = "DELETE FROM books WHERE id = %s" % self.id
                cursor.execute(sql)
                db.connector.commit()
        except Exception as err:
            db.connector.rollback()
            print('error in delete book')
            print(str(err))

    @classmethod
    def get_all_books(cls):
        try:
            with db.connector.cursor() as cursor:
                sql = 'SELECT * from books'
                cursor.execute(sql)
                results = cursor.fetchall()
                books = list()
                for book in results:
                    books.append(Book(book[1], book[2], book[3], book[0]))
                return books
        except Exception as err:
            print('error in get all books')
            print(str(err))

    @classmethod
    def get_book_by_id(cls, ID):
        try:
            with db.connector.cursor() as cursor:
                sql = 'SELECT * from books WHERE id = %s' % ID
                cursor.execute(sql)
                result = cursor.fetchone()
                return Book(result[1], result[2], result[3], result[0])
        except Exception as err:
            print('error in get book by id')
            print(str(err))


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=False)
    name = db.Column(db.String(64))
    avatar_hash = db.Column(db.String(32))


class Developer(db.Model):
    __tablename__ = 'developers'
    id = db.Column(db.Integer, primary_key=True)
    introduction = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    authorization_form = db.relationship('AuthorizationForm', uselist=False, backref='applicant')
    applications = db.relationship('Application', backref='developer')


class Administrator(db.Model):
    __tablename__ = 'administrators'
    id = db.Column(db.Integer, primary_key=True)
    introduction = db.Column(db.String(128))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    authorization_forms = db.relationship('AuthorizationForm', backref='approver')


class AuthorizationForm(db.Model):
    __tablename__ = 'authorization_forms'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(32), nullable=False)
    reason = db.Column(db.String(128))
    applicant_id = db.Column(db.Integer, db.ForeignKey('developers.id'))
    approver_id = db.Column(db.Integer, db.ForeignKey('administrators.id'))


class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    description = db.Column(db.String(128))
    status = db.Column(db.String(32), nullable=False)
    language = db.Column(db.String(64), nullable=False)
    cpu_priority = db.Column(db.Integer, nullable=False)
    memory = db.Column(db.Integer, nullable=False)
    disk = db.Column(db.Integer, nullable=False)
    bandwidth_priority = db.Column(db.Integer, nullable=False)
    developer_id = db.Column(db.Integer, db.ForeignKey('developers.id'))

    messages = db.relationship('Message', backref='application')
    interfaces = db.relationship('Interface', backref='application')
    implementation_files = db.relationship('ImplementationFile', backref='application')
    images = db.relationship('Image', backref='application')
    services = db.relationship('Service', backref='application')


class Message(db.Model):
    __tablename__ = 'messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    type = db.Column(db.Integer, nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))
    message_items = db.relationship('MessageItem', backref='Message')


class MessageItem(db.Model):
    __tablename__ = 'message_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    type = db.Column(db.Integer, nullable=False)
    order = db.Column(db.Integer, unique=True)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'))


class Interface(db.Model):
    __tablename__ = 'interfaces'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))
    input_message_id = db.Column(db.Integer, db.ForeignKey('messages.id'))
    output_message_id = db.Column(db.Integer, db.ForeignKey('messages.id'))


class ImplementationFile(db.Model):
    __tablename__ = 'implementation_files'
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(64), nullable=False)
    upload_timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    file_path = db.Column(db.String(128), nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    type = db.Column(db.String(32), nullable=False)
    build_timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    image_ref = db.Column(db.String(128), nullable=False)
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))


edge_node_relationship = db.Table('edge_node_relationships',
                                  db.Column('main_node_id', db.Integer, db.ForeignKey('edge_nodes.id'), primary_key=True),
                                  db.Column('nearby_node_id', db.Integer, db.ForeignKey('edge_nodes.id'), primary_key=True))


class EdgeNode(db.Model):
    __tablename__ = 'edge_nodes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    ip = db.Column(db.String(32), nullable=False)
    port = db.Column(db.Integer, nullable=False)
    power_type = db.Column(db.String(32))
    console_type = db.Column(db.String(32))
    status = db.Column(db.String(32), nullable=False)
    cpu_capacity = db.Column(db.Integer, nullable=False)
    memory_capacity = db.Column(db.Integer, nullable=False)
    disk_capacity = db.Column(db.Integer, nullable=False)
    bandwidth_capacity = db.Column(db.Integer, nullable=False)
    administrator_id = db.Column(db.Integer, db.ForeignKey('administrators.id'))
    available_resources = db.relationship('Resource', backref='edge_node')
    records = db.relationship('Record', backref='edge_node')
    logs = db.relationship('Log', backref='edge_node')
    nearby_nodes = db.relationship("EdgeNode", secondary=edge_node_relationship,
                                   primaryjoin=(id == edge_node_relationship.c.main_node_id),
                                   secondaryjoin=(id == edge_node_relationship.c.nearby_node_id))


class Resource(db.Model):
    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    available_value = db.Column(db.Integer, nullable=False)
    edge_node_id = db.Column(db.Integer, db.ForeignKey('edge_nodes.id'))


class Service(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    status = db.Column(db.String(32), nullable=False)
    container_ref = db.Column(db.String(128))
    ip = db.Column(db.String(32))
    port = db.Column(db.Integer)
    image_id = db.Column(db.Integer, db.ForeignKey('images.id'))
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))


class Record(db.Model):
    __tablename__ = 'records'
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(32), nullable=False, index=True)
    start_timestamp = db.Column(db.DateTime, index=True)
    end_timestamp = db.Column(db.DateTime, index=True)
    user_info = db.Column(db.String(512))
    application_id = db.Column(db.Integer, db.ForeignKey('applications.id'))
    edge_node_id = db.Column(db.Integer, db.ForeignKey('edge_nodes.id'))

    calls = db.relationship('Call', backref='record')


class Call(db.Model):
    __tablename__ = 'calls'
    id = db.Column(db.Integer, primary_key=True)
    method_name = db.Column(db.String(64), nullable=False)
    start_timestamp = db.Column(db.DateTime, index=True)
    end_timestamp = db.Column(db.DateTime, index=True)
    status = db.Column(db.String(32), nullable=False)
    record_id = db.Column(db.Integer, db.ForeignKey('records.id'))


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32), nullable=False, index=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    content = db.Column(db.String(512), nullable=False)
    edge_node_id = db.Column(db.Integer, db.ForeignKey('edge_nodes.id'))


class SystemParameter(db.Model):
    __tablename__ = 'system_parameters'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(32), nullable=False)
    value = db.Column(db.String(512), nullable=False)
