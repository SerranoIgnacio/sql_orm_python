#!/usr/bin/env python
'''
SQL Introducción [Python]
Ejercicios de práctica
---------------------------
Autor: Inove Coding School
Version: 1.1

Descripcion:
Programa creado para poner a prueba los conocimientos
adquiridos durante la clase
'''

__author__ = "Inove Coding School"
__email__ = "alumnos@inove.com.ar"
__version__ = "1.1"

import sqlite3
from unicodedata import name

import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Crear el motor (engine) de la base de datos
engine = sqlalchemy.create_engine("sqlite:///secundaria.db")
base = declarative_base()


class Tutor(base):
    __tablename__ = "tutor"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    
    def __repr__(self):
        return f"Tutor: {self.name}"


class Estudiante(base):
    __tablename__ = "estudiante"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    grade = Column(Integer)
    tutor_id = Column(Integer, ForeignKey("tutor.id"))

    tutor = relationship("Tutor")

    def __repr__(self):
        return f"Estudiante: {self.name}, edad {self.age}, grado {self.grade}, tutor {self.tutor.name}"


def create_schema():
    # Borrar todos las tablas existentes en la base de datos
    # Esta linea puede comentarse sino se eliminar los datos
    base.metadata.drop_all(engine)

    # Crear las tablas
    base.metadata.create_all(engine)

def insert_tutor(name):
    Session = sessionmaker(bind=engine)
    session = Session()

    tutor = Tutor(name=name)

    session.add(tutor)
    session.commit()
    print(tutor)

def insert_estudiante(name, age, grade, tutor):
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(Tutor).filter(Tutor.name == tutor)
    tutor_existe = query.first()

    if tutor_existe is None:
        print(f"Error al añadir al estudiante {name}, no existe el tutor {tutor}")
        return

    estudiante = Estudiante(name=name, age=age, grade=grade, tutor=tutor_existe )

    session.add(estudiante)
    session.commit()
    print(estudiante)


def fill():
    print('Completemos esta tablita!')
    # Llenar la tabla de la secundaria con al munos 2 tutores
    # Cada tutor tiene los campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del tutor (puede ser solo nombre sin apellido)
    insert_tutor('Jaime')
    insert_tutor('Pascual')
    # Llenar la tabla de la secundaria con al menos 5 estudiantes
    # Cada estudiante tiene los posibles campos:
    # id --> este campo es auto incremental por lo que no deberá completarlo
    # name --> El nombre del estudiante (puede ser solo nombre sin apellido)
    # age --> cuantos años tiene el estudiante
    # grade --> en que año de la secundaria se encuentra (1-6)
    # tutor --> el tutor de ese estudiante (el objeto creado antes)
    insert_estudiante("Cristian", 24, 5, "Pascual")
    insert_estudiante('Jose', 28, 2, 'Pascual')
    insert_estudiante('Alvaro', 14, 1, 'Jaime')
    insert_estudiante('Paul', 27, 2, 'Pascual')
    insert_estudiante('Ivan', 20, 2, 'Jaime')
    insert_estudiante('Nilo', 24, 2, 'Jaime')
    # No olvidarse que antes de poder crear un estudiante debe haberse
    # primero creado el tutor.


def fetch():
    print('Comprobemos su contenido, ¿qué hay en la tabla?')
    # Crear una query para imprimir en pantalla
    # todos los objetos creaods de la tabla estudiante.
    # Imprimir en pantalla cada objeto que traiga la query
    # Realizar un bucle para imprimir de una fila a la vez
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(Estudiante)
    for estudiante in query:
        print(estudiante)
    


def search_by_tutor(tutor):
    print('Operación búsqueda!')
    # Esta función recibe como parámetro el nombre de un posible tutor.
    # Crear una query para imprimir en pantalla
    # aquellos estudiantes que tengan asignado dicho tutor.

    # Para poder realizar esta query debe usar join, ya que
    # deberá crear la query para la tabla estudiante pero
    # buscar por la propiedad de tutor.name
    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(Estudiante).join(Estudiante.tutor).filter(Tutor.name == tutor)
    print(f"Los estudiante que tienen al tutor {tutor} son:")
    for estudiante in query:
        print(estudiante.name)


def modify(id, name):
    print('Modificando la tabla')
    # Deberá actualizar el tutor de un estudiante, cambiarlo para eso debe
    # 1) buscar con una query el tutor por "tutor.name" usando name
    # pasado como parámetro y obtener el objeto del tutor
    Session = sessionmaker(bind=engine)
    session = Session()
    query = session.query(Tutor).filter(Tutor.name == name)
    tutor = query.first()

    # 2) buscar con una query el estudiante por "estudiante.id" usando
    # el id pasado como parámetro
    query = session.query(Estudiante).filter(Estudiante.id == id)
    estudiante = query.first()

    # 3) actualizar el objeto de tutor del estudiante con el obtenido
    # en el punto 1 y actualizar la base de datos
    estudiante.tutor = tutor
    session.add(estudiante)
    session.commit()
    print(f"Estudiante actualizado {estudiante.name} con el tutor {name}")

    # TIP: En clase se hizo lo mismo para las nacionalidades con
    # en la función update_persona_nationality

def count_grade(grade):
    print('Estudiante por grado')
    # Utilizar la sentencia COUNT para contar cuantos estudiante
    # se encuentran cursando el grado "grade" pasado como parámetro
    # Imprimir en pantalla el resultado
    Session = sessionmaker(bind=engine)
    session = Session()

    result = session.query(Estudiante).filter(Estudiante.grade == grade).count()
    print(f'Estudiantes que se encuentran cursando el grado {grade}= {result} estudiantes')

    # TIP: En clase se hizo lo mismo para las nacionalidades con
    # en la función count_persona


if __name__ == '__main__':
    print("Bienvenidos a otra clase de Inove con Python")
    create_schema()   # create and reset database (DB)
    fill()
    fetch()

    tutor = 'Pascual'
    search_by_tutor(tutor)

    nuevo_tutor = 'Nacho'
    id = 2
    modify(id, nuevo_tutor)

    grade = 2
    count_grade(grade)
