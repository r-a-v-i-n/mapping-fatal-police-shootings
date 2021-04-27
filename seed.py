# input code to pull from dataset

import os
import csv
import crud
from server import app
from model import Wapo, db, connect_to_db
import datetime
from faker import Faker
from random import randint
fake = Faker()


# write helper functions here
def cast_int(str):
    try:
        n = int(str)
        return n
    except (ValueError, TypeError):
        return None

def cast_float(str):
    try:
        n = float(str)
        return n
    except (ValueError, TypeError):
        return None

# #pull wapo data from csv file
def seed_csv_data(filename):
    with open(filename, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            # if the key at this value is "True", set it to the boolean True instead
            if row['signs_of_mental_illness'] == "True":
                row['signs_of_mental_illness'] = True
            else: 
                row['signs_of_mental_illness'] = False
            if row['body_camera'] == 'True':
                row['body_camera'] = True
            else:
                row['body_camera'] = False
            # if row['is_geocoding_exact'] == 'True':
            #     row['is_geocoding_exact'] = True
            # else:
            #     row['is_geocoding_exact'] = False
            for key in row:
                if row[key] == '':
                    row[key] = None
            record = Wapo(
            data_id = cast_int(row['data_id']),
            name = row['name'],
            date = datetime.datetime.strptime(row['date'], "%Y-%m-%d").date(),
            manner_of_death = row['manner_of_death'],
            allegedly_armed = row['allegedly_armed'],
            age = cast_int(row['age']),
            gender = row['gender'],
            race = row['race'],
            city = row['city'],
            state = row['state'],
            signs_of_mental_illness = row['signs_of_mental_illness'],
            alleged_threat_level = row['alleged_threat_level'],
            allegedly_fleeing = row['allegedly_fleeing'],
            body_camera = row['body_camera'],
            longitude = cast_float(row['longitude']),
            latitude = cast_float(row['latitude']))
            # is_geocoding_exact = row['is_geocoding_exact'])
            db.session.add(record)
            db.session.commit()
    csv_file.close()


def seed_users():
    for i in range(9):
        name = fake.name().split()
        username = ''.join(name)
        password = fake.password()
        email = fake.email()
        city = fake.city()
        state = fake.state()
        crud.create_user(username, password, email, city, state)


def seed_orgs():
    for i in range(2):
        org_name = fake.company()
        url  = fake.url()
        email = fake.email()
        phone = fake.phone_number()
        city = fake.city()
        state = fake.state()
        user_id = randint(1, 10)
        crud.create_org(org_name, url, email, phone, city, state, user_id)


# # stretch goal - pull from updating dataset in WaPo (not MVP)

if __name__ == '__main__':
    

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.
    
    os.system('dropdb wapo')
    os.system('createdb wapo')
    connect_to_db(app)
    db.create_all()
    seed_csv_data('wapo_data.csv')
    seed_users()
    seed_orgs()
    # uncomment if model.py + fake users & fake orgs aren't solid
