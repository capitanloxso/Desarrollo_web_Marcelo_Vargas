import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "tarea_2_cc5002"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://cc5002:programacionweb@localhost:3306/tarea2?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
