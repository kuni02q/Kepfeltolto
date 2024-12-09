
# Kepfeltolto

## A "Best Gallery" projekt indítása

Ez a dokumentáció bemutatja, hogyan állíthatod be és indíthatod el a "Best Gallery" nevű Django alapú webalkalmazást a saját gépeden.

### **Sükséges csomagok telepítése**

```bash
pip install django
```

### Az adatbázis és a szükséges táblák létrehozásához futtasd a migrációkat:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Szuperuser létrehozása (adminisztrátor fiók)

Az admin felület eléréséhez hozz létre egy szuperuser fiókot:

```bash
python manage.py createsuperuser
```

Add meg a kért adatokat (felhasználónév, e-mail cím, jelszó).

### Django fejlesztői szerver indítása

```bash
python manage.py runserver
```

A szerver alapértelmezés szerint a [http://127.0.0.1:8000/](http://127.0.0.1:8000/) címen lesz elérhető.

---

## Funkcionális Specifikáció

### 1. Áttekintés

A Best Gallery egy egyszerű és letisztult webalapú képmegosztó alkalmazás, amely lehetővé teszi a felhasználók számára képek feltöltését, megosztását és más felhasználók képeinek megtekintését. Célunk egy olyan közösségi platform létrehozása, ahol a felhasználók felfedezhetik és megoszthatják vizuális tartalmaikat, valamint interakcióba léphetnek egymással a like/dislike funkciók segítségével. Az alkalmazás felhasználóbarát felületet kínál, támogatva a modern webes technológiákat és különböző eszközökön is kényelmesen használható.

### 2. Jelenlegi helyzet

A jelenlegi képmegosztó platformok gyakran bonyolultak, túlterheltek funkciókkal vagy nem kínálnak elegendő személyre szabhatóságot. Sok felhasználó szeretne egy egyszerűbb, letisztultabb felületet, ahol a fókusz a képek megosztásán és felfedezésén van. A Best Gallery célja, hogy ezt az igényt kielégítse egy egyszerű, de hatékony alkalmazással.

### 3. Követelménylista (módosított)

Az alábbiakban található a rendszer funkcióinak listája, amelyből eltávolítottuk a jelszó módosítási, elfelejtett jelszó és üzenetküldési funkciókat, valamint hozzáadtunk egy új funkciót a tartalom moderálására.

| Modul ID | Név                  | Kifejtés                                                                 |
|----------|-----------------------|---------------------------------------------------------------------------|
| K1       | Regisztráció          | A felhasználó új fiókot hozhat létre felhasználónév, email cím és jelszó megadásával. |
| K2       | Bejelentkezés         | A felhasználó bejelentkezhet a rendszerbe felhasználónév és jelszó megadásával.         |
| K3       | Profil szerkesztése   | A felhasználó szerkesztheti saját profilját: feltölthet profilképet, megadhat bemutatkozó szöveget. |
| K4       | Kép feltöltése        | A felhasználó képeket tölthet fel a rendszerbe. Megadhatja a kép címét, leírását, kategóriáját és címkéket rendelhet hozzá. |
| K5       | Képek megtekintése   | A felhasználó megtekintheti a feltöltött képeket, beleértve a kép nagyított változatát, címét, leírását, címkéit és a feltöltő adatait. |
| K6       | Kép törlése          | A felhasználó törölheti saját feltöltött képeit. A törlés előtt megerősítést kér a rendszer. |
| K7       | Képek keresése       | A felhasználó kereshet képeket cím, leírás vagy címkék alapján.                           |
| K8       | Felhasználók keresése | A felhasználó kereshet más felhasználókra, megtekintheti azok profilját és feltöltött képeit.      |
| K10      | Kedvencek kezelése    | A felhasználó kedvencekhez adhatja a számára tetsző képeket, és megtekintheti saját kedvenceinek listáját. |
| K14      | Téma váltás          | A felhasználó igényei szerint cserélheti a témát világos és sötét között. |
| K15      | Segítség és támogatás| A felhasználók hozzáférhetnek egy súgóoldalhoz, ahol információkat találnak az alkalmazás használatáról. |
| K16      | Tartalom moderálás    | Az adminisztrátorok felügyelhetik és moderálhatják a feltöltött képeket, hogy biztosítsák a tartalom megfelelőségét a közösségi irányelveknek. |

### Like-olás és dislike-olás

A felhasználó egy kép részletező oldalán like-olhatja (tetszik) vagy dislike-olhatja (nem tetszik) a képet. A like és dislike státusz tárolódik az adatbázisban. Ha a felhasználó először dislike-olta a képet, majd like-olni szeretné, a rendszer először eltávolítja a dislike-ot, majd hozzáadja a like-ot, és fordítva. Erről a kép tulajdonosa értesítést kap (pl. a like vagy dislike eseményről).

### Értesítések a like/dislike eseményekről

Ha egy felhasználó like-olja vagy dislike-olja a másik felhasználó képét, a kép tulajdonosa értesítést kap. Az értesítések megjelennek az "Inbox" nézetben, ahol a felhasználó megtekintheti, ki és melyik képén hajtott végre like-ot vagy dislike-ot.

---

### 4. Jelenlegi üzleti folyamatok modellje

A mai képmegosztó platformok sok esetben nem felelnek meg a felhasználók egyszerűség és használhatóság iránti igényeinek. Gyakran túl sok funkcióval rendelkeznek, amelyek elvonják a figyelmet a lényegi tartalomtól. Nincs olyan platform, amely egyszerűen használható, letisztult felülettel rendelkezik, és a közösségi interakciókra helyezi a hangsúlyt.

---

### 5. Igényelt üzleti folyamatok modellje

A Best Gallery célja egy olyan képmegosztó platform létrehozása, amely egyszerű és felhasználóbarát. A felhasználók könnyedén tölthetnek fel és oszthatnak meg képeket, felfedezhetik mások alkotásait, és interakcióba léphetnek egymással. Az alkalmazás támogatja a kategóriákat és címkéket, amelyek megkönnyítik a tartalmak rendszerezését és keresését. Az adminisztrátorok számára a tartalom moderálási funkció biztosítja, hogy a feltöltött képek megfeleljenek a közösségi irányelveknek. Az alkalmazás különböző eszközökön is jól használható.

---

### 6. Használati esetek

**Felhasználó:**
- Regisztráció (K1)
- Bejelentkezés (K2)
- Profil szerkesztése (K3)
- Képek feltöltése és törlése (K4, K6)
- Képek böngészése és keresése (K5, K7)
- Kedvencek kezelése (K10)
- Képek like-olása és dislike-olása (K5 részletesebben)
- Téma váltás (K14)
- Segítség és támogatás (K15)

**Adminisztrátor:**
- Felhasználók és tartalmak felügyelete
- Kategóriák és címkék kezelése
- Tartalom moderálása (K16)
- Rendszerkarbantartás

---

### 7. Megfeleltetés, hogyan fedik le a használati esetek a követelményeket

| Használati eset       | Követelmény(ek) |
|-------------------------|-------------------|
| Regisztráció          | K1               |
| Bejelentkezés         | K2               |
| Profil szerkesztése   | K3               |
| Képek feltöltése     | K4               |
| Képek megtekintése    | K5, K7           |
| Képek keresése       | K7               |
| Felhasználók keresése | K8               |
| Kedvencek kezelése    | K10              |
| Téma váltás         | K14              |
| Segítség és támogatás| K15              |
| Tartalom moderálása    | K16              |

---

### 8. Forgatókönyv

**Forgatókönyv 1: Kép feltöltése**

1. A felhasználó bejelentkezik.
2. A navigációs menüben kiválasztja a "Kép feltöltése" opciót.
3. Kiválaszt egy képfájlt a számítógépéről.
4. Megadja a kép címét, leírását, kategóriáját és címkéit.
5. Rákattint a "Feltöltés" gombra.
6. A rendszer ellenőrzi a feltöltött fájlt, majd elmenti az adatbázisba.

**Forgatókönyv 2: Like-olás és értesítés**

1. A felhasználó bejelentkezik.
2. Megnyit egy tetszőleges képet.
3. Rákattint a "Tetszik" gombra. Ha korábban "Nem tetszik" volt, a rendszer törli azt, majd hozzáadja a like-ot.
4. A kép tulajdonosa az Inbox-ban értesítést kap arról, hogy valaki like-olta a képét.



