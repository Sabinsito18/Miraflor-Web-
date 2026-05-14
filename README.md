# A.C.D. Miraflor

Web del club con páginas de inicio, equipo, calendario, noticias e inscripciones.

## Arrancar con MySQL

1. Importa `data/miraflor_mysql.sql` en MySQL si todavía no tienes las tablas.
2. Crea un archivo `.env` copiando `.env.example`.
3. Rellena tus datos reales de MySQL.
4. Instala dependencias:

```powershell
py -m pip install -r requirements.txt
```

5. Sincroniza jugadores y partidos iniciales sin borrar inscripciones:

```powershell
py scripts\sync_mysql.py
```

6. Arranca el servidor:

```powershell
py server.py
```

7. Abre la web desde:

```text
http://127.0.0.1:8000
```

No abras los archivos HTML directamente, porque el formulario necesita el servidor para guardar en MySQL.

## Comprobar conexión

Abre:

```text
http://127.0.0.1:8000/api/health
```

Debe devolver:

```json
{"ok": true, "database": "mysql"}
```
