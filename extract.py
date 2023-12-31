import pathlib
import shutil

import psycopg2

connection = psycopg2.connect("dbname=ricardoboix.com host=db.h2.int.pdp7.net user=alex@IPA.PDP7.NET")
connection.set_client_encoding("UTF8")

cursor = connection.cursor()
cursor.execute("select titulo from poemas")

poemas = pathlib.Path("poemas")
shutil.rmtree(poemas, ignore_errors=True)
poemas.mkdir()


for row in cursor.fetchall():
    titulo, = row

    poema_file = poemas / f"{titulo}.md"

    cursor2 = connection.cursor()
    cursor2.execute("select texto, audio from poemas where titulo = %s", (titulo,))

    with open(poema_file, "w") as f:
        texto, audio = cursor2.fetchall()[0]
        def _map_line(l):
            l = l.strip()
            if l:
                l += "  "  # for poems, this is a br
            return l
        texto = "\n".join(map(_map_line, texto.splitlines()))
        if audio:
            texto += f"\n\naudio:{audio}\n"
        f.write(texto)


cursor = connection.cursor()
cursor.execute("select * from relatos")


relatos = pathlib.Path("relatos_md")
shutil.rmtree(relatos, ignore_errors=True)
relatos.mkdir()


for row in cursor.fetchall():
    titulo, texto = row
    relato_file = relatos / f"{titulo}.md"
    with open(relato_file, "w") as f:
        texto = "\n".join(map(str.strip, texto.splitlines())) + "\n"
        f.write(texto)
