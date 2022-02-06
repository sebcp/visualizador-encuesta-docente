import requests
import json

from bs4 import BeautifulSoup

from constants import *

def dump_ids(year, semester, depts):
    dept_ids = {}
    for key in depts.keys():
        link = f"https://ucampus.uchile.cl/m/fcfm_catalogo/?semestre={year}{semester}&depto={key}"
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')

        imgs = soup.find_all("img", class_="photo foto chica")
        ids = []
        for img in imgs:
            id = str(img).split("/")[7]
            if id not in ids and len(id) == 32:
                ids.append(id)
        dept_ids[key] = ids

    with open('dept_ids.json', 'w') as fp:
        json.dump(dept_ids, fp)

def dump_courses(year, semester, depts):
    dept_id = {}
    for key in depts:
        link = f"https://ucampus.uchile.cl/m/fcfm_catalogo/?semestre={year}{semester}&depto={key}"
        response = requests.get(link)
        soup = BeautifulSoup(response.content, 'html.parser')

        courses = soup.find_all("div", class_="ramo") # sacamos contenedores de ramos
        ids = {}
        for course in courses:
            h1 = course.find_all("h1") # sacamos contenedores h1
            for i in range(len(h1)):
                if i % 2 == 1: # impares contienen id y nombre del docente
                    item = h1[i] # sacamos el html
                    photo = item.find_all("img", class_="photo foto chica") # buscamos las instancias de img
                    name = str(item).split(">")[2].split("<")[0] # sacamos el nombre del docente
                    if photo: # si el arreglo tiene contenido
                        id = str(photo).split("/")[7] # sacamos el id de ucursos del docente
                        id_ramo = course.find("h2") # sacamos el contendor h2
                        course_code = str(id_ramo).split('"')[1] # sacamos el código del curso
                        if id not in ids:
                            ids[id] = {} # inicializamos el diccionario del docente
                        if "courses" not in ids[id]:
                            ids[id]["courses"] = {} # inicializamos el diccionario de los cursos del docente
                        if len(id) == 32 and course_code not in ids[id]["courses"]:
                            ids[id]["name"] = name
                            h2 = str(course.find_all("h2")[0])
                            course_name = ' '.join(h2.split(">")[1].split("<")[0].split(" ")[1:]).split("\n")[0]
                            ids[id]["courses"][course_code] = course_name
        dept_id[key] = ids

        with open('dept_ids.json', 'w', encoding='utf-8') as fp:
            json.dump(dept_id, fp, ensure_ascii=False)

#dump_courses(YEAR, SEMESTER, DEPTS)