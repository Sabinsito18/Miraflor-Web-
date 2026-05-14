# Publicar la web de A.C.D. Miraflor

Esta web necesita un hosting que ejecute Python, porque el formulario guarda inscripciones en SQLite.

## Opcion recomendada

1. Sube este proyecto a GitHub.
2. Crea un servicio web en Render, Railway o PythonAnywhere.
3. Usa estos comandos:

```bash
python scripts/init_db.py
python server.py
```

En Render, el archivo `render.yaml` ya deja preparada la configuracion:

- Build command: `python scripts/init_db.py`
- Start command: `python server.py`
- Variable `HOST`: `0.0.0.0`

El hosting asignara automaticamente la variable `PORT`.

## Dominio

Cuando el hosting te de una URL publica, compra o usa un dominio y apunta sus DNS al hosting:

- `www.tudominio.com` con CNAME hacia la URL del hosting.
- Dominio raiz, si lo quieres, con A/ALIAS segun indique tu proveedor.

## Importante

SQLite es suficiente para una web pequena, pero en algunos hostings gratuitos el disco puede reiniciarse. Si el club empieza a recibir inscripciones reales, conviene mover `inscripciones` a una base persistente tipo PostgreSQL.
