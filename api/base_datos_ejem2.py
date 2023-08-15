import sqlite3
from fastapi import FastAPI
from pydantic import BaseModel

conn = sqlite3.connect("libros.db")

cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS libros(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               titulo TEXT NOT NULL,
               creadores TEXT NOT NULL,
               imagenes TEXT NOT NULL,
               ligas TEXT NOT NULL,
               precio TEXT NOT NULL
               )''')

conn.commit()
conn.close()

class Datos(BaseModel):
    titulo: str
    creadores: str
    imagenes: str
    ligas: str
    precio: str

app = FastAPI()

@app.post("/agregar/")
async def agregar_datos(datos: Datos):
    conn = sqlite3.connect("libros.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO libros (titulo, creadores, imagenes, ligas, precio) VALUES (?, ?, ?, ?, ?)", (datos.titulo, datos.creadores, datos.imagenes, datos.ligas, datos.precio))
    conn.commit()
    conn.close()
    return {"mensaje": "Datos agregados exitosamente"}

@app.get("/datos/")
async def obtener_todos_datos():
    conn = sqlite3.connect("libros.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM libros")
    resultados = cursor.fetchall()
    conn.close()
    if resultados:
        return [{"id": resultado[0], "titulo": resultado[1], "creadores": resultado[2], "imagenes": resultado[3], "ligas": resultado[4], "precio": resultado[5]} for resultado in resultados]
    else:
        return {"mensaje": "No hay datos en la base de datos"}

@app.get("/consultar/{id}/")
async def consultar_datos(id: int):
    conn = sqlite3.connect("libros.db")
    cursor = conn.cursor()
    cursor.execute("SELECT titulo, creadores, imagenes, ligas, precio FROM libros WHERE id=?", (id,))
    resultado = cursor.fetchone()
    conn.close()
    if resultado:
        return {"titulo": resultado[0], "creadores": resultado[1], "imagenes": resultado[2], "ligas": resultado[3], "precio": resultado[4]}
    else:
        return {"mensaje": "Dato no encontrado"}
    

@app.put("/actualizar/{id}/")
async def actualizar_datos(id:int, datos: Datos):
    conn = sqlite3.connect("libros.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE libros SET titulo=?, creadores=?, imagenes=?, ligas=?, precio=? WHERE id=?", (datos.titulo,datos.creadores, datos.imagenes, datos.ligas, datos.precio))
    resultado = cursor.fetchone()
    conn.close()
    return {"mensaje": "Datos actualizados exitosamente"}

@app.delete("/eliminar/{id}/")
async def eliminar_datos(id: int):
    conn = sqlite3.connect("libros.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM libros WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return {"mensaje": "Datos eliminados exitosamente"}
