
# Kepfeltolto
=======
## A "Best Gallery" projekt indítása
Ez a dokumentáció bemutatja, hogyan állíthatod be és indíthatod 
el a "Best Gallery" nevű Django alapú webalkalmazást a saját gépeden.

**Szükséges csomagok telepítése**

```bash
pip install django
```

**Az adatbázis és a szükséges táblák létrehozásához futtasd a migrációkat:**


```bash

python manage.py makemigrations
python manage.py migrate
```
**Szuperuser létrehozása (adminisztrátor fiók)**

Az admin felület eléréséhez hozz létre egy szuperuser fiókot:

```bash
python manage.py createsuperuser
```
Add meg a kért adatokat (felhasználónév, e-mail cím, jelszó).

**Indítsd el a Django fejlesztői szervert:**

```bash
python manage.py runserver
```
A szerver alapértelmezés szerint a http://127.0.0.1:8000/ címen lesz elérhető.
