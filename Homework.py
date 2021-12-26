import sqlite3
import pandas as pd
import re


def get_out_tags(field):
    return re.sub(r'\<[^>]*\>', '', str(field))


def create_qualifications():
    con = sqlite3.connect('works.sqlite')
    cursor = con.cursor()
    # Таблица с квалификациями
    cursor.execute('DROP TABLE IF EXISTS qualifications')
    cursor.execute('CREATE TABLE qualifications(qualification TEXT PRIMARY KEY )')
    cursor.execute(
        'INSERT INTO qualifications SELECT DISTINCT qualification FROM works WHERE qualification IS NOT NULL')
    con.commit()


def create_job_titles():
    con = sqlite3.connect('works.sqlite')
    cursor = con.cursor()
    # Таблица с названиями работы
    cursor.execute('DROP TABLE IF EXISTS jobTitles')
    cursor.execute('CREATE TABLE jobTitles(jobTitle TEXT PRIMARY KEY )')
    cursor.execute('INSERT INTO jobTitles SELECT DISTINCT jobTitle FROM works WHERE jobTitle IS NOT NULL')
    con.commit()


def create_education():
    con = sqlite3.connect('works.sqlite')
    cursor = con.cursor()
    # Таблица с образованиями
    cursor.execute('DROP TABLE IF EXISTS educations')
    cursor.execute('CREATE TABLE educations(educationType TEXT PRIMARY KEY )')
    cursor.execute(
        'INSERT INTO educations SELECT DISTINCT educationType FROM works WHERE works.educationType IS NOT NULL')
    con.commit()


def create_genders():
    con = sqlite3.connect('works.sqlite')
    cursor = con.cursor()
    # Таблица с гендерами
    cursor.execute('DROP TABLE IF EXISTS genders')
    cursor.execute('CREATE TABLE genders(gender TEXT PRIMARY KEY )')
    cursor.execute('INSERT INTO genders SELECT DISTINCT gender FROM works WHERE gender IS NOT NULL')
    con.commit()
    return cursor


def create_works():
    con = sqlite3.connect('works.sqlite')
    cursor = con.cursor()
    cursor.execute('drop table if exists works')
    cursor.execute(
        'create table if not exists works (ID INTEGER PRIMARY KEY AUTOINCREMENT,salary INTEGER,educationType TEXT,'
        'jobTitle TEXT,qualification TEXT,gender TEXT,dateModify TEXT,skills TEXT,otherInfo TEXT)')
    con.commit()

    # Скиллы и otherInfo
    df = pd.read_csv('works.csv')
    df['skills'] = df['skills'].apply(get_out_tags)
    df['otherInfo'] = df['otherInfo'].apply(get_out_tags)
    df.to_sql('works', con, if_exists='append', index=False)
    con.commit()


create_works()
create_genders()
create_job_titles()
create_education()
create_qualifications()
