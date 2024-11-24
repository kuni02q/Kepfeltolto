
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

# Kepfeltolto

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


# Best Gallery

## Funkcionális Specifikáció

### 1. Áttekintés
A Best Gallery egy webalapú képmegosztó alkalmazás, amely lehetővé teszi a felhasználók számára képek feltöltését, megosztását és más felhasználók képeinek megtekintését. Célunk egy olyan közösségi platform létrehozása, ahol a felhasználók felfedezhetik és megoszthatják vizuális tartalmaikat, valamint kapcsolatba léphetnek egymással. Az alkalmazás egyszerű és felhasználóbarát felületet kínál, támogatva a modern webes technológiákat és reszponzív dizájnnal rendelkezik, így különböző eszközökön is kényelmesen használható.

### 2. Jelenlegi helyzet
A jelenlegi képmegosztó platformok gyakran bonyolultak, túlterheltek funkciókkal, vagy nem kínálnak elegendő személyre szabhatóságot. Sok felhasználó szeretne egy egyszerűbb, letisztultabb felületet, ahol a fókusz a képek megosztásán és felfedezésén van. A Best Gallery célja, hogy ezt az igényt kielégítse egy egyszerű, de hatékony alkalmazással.

### 3. Követelménylista
Az alábbiakban található a rendszer funkcióinak listája:

| Modul ID | Név | Kifejtés |
|----------|------|-----------|
| K1 | Regisztráció | A felhasználó új fiókot hozhat létre felhasználónév, email cím és jelszó megadásával. A jelszavakat biztonságosan, kódolva tároljuk az adatbázisban. Hibás vagy hiányos adatok esetén a rendszer hibaüzenetet jelenít meg. |
| K2 | Bejelentkezés | A felhasználó bejelentkezhet a rendszerbe email címe és jelszava megadásával. Ha a megadott adatok helytelenek, hibaüzenetet kap. |
| K3 | Profil szerkesztése | A felhasználó szerkesztheti saját profilját: feltölthet profilképet, megadhat bemutatkozó szöveget, módosíthatja személyes adatait, például születési dátumát. |
| K4 | Kép feltöltése | A felhasználó képeket tölthet fel a rendszerbe. Megadhatja a kép címét, leírását, kategóriáját és címkéket (tageket) rendelhet hozzá. A képek feltöltésekor a rendszer ellenőrzi a fájlformátumot és méretet. |
| K5 | Képek megtekintése | A felhasználó megtekintheti a feltöltött képeket, beleértve a kép nagyított változatát, címét, leírását, címkéit és a feltöltő adatait. |
| K6 | Kép törlése | A felhasználó törölheti saját feltöltött képeit. A törlés előtt megerősítést kér a rendszer a véletlen adatvesztés elkerülése érdekében. |
| K7 | Képek keresése | A felhasználó kereshet képeket cím, leírás vagy címkék alapján. A keresési eredmények listázása és rendezése különböző szempontok szerint (pl. feltöltés dátuma, népszerűség) lehetséges. |
| K8 | Felhasználók keresése | A felhasználó kereshet más felhasználókra, megtekintheti azok profilját és feltöltött képeit. |
| K9 | Üzenetküldés | A felhasználó privát üzeneteket küldhet más felhasználóknak. Az üzenetek olvasott/olvasatlan státusszal rendelkeznek. |
| K10 | Kedvencek kezelése | A felhasználó kedvencekhez adhatja a számára tetsző képeket, és megtekintheti saját kedvenceinek listáját. |
| K11 | Jelszó módosítása | A felhasználó módosíthatja saját jelszavát. Ehhez meg kell adnia a régi jelszót, az új jelszót és annak megerősítését. |
| K12 | Elfelejtett jelszó | Ha a felhasználó elfelejtette jelszavát, emailben kérhet jelszó-visszaállítást. A rendszer biztonságosan kezeli a jelszó visszaállítását. |
| K13 | Reszponzív dizájn | Az alkalmazás reszponzív kialakítású, így különböző eszközökön (asztali gép, tablet, mobiltelefon) is megfelelően jelenik meg és használható. |
| K14 | Téma váltás | A felhasználó igényei szerint cserélheti a témát világos és sötét között. |
| K15 | Segítség és támogatás | A felhasználók hozzáférhetnek egy súgóoldalhoz, ahol információkat találnak az alkalmazás használatáról, valamint kapcsolatba léphetnek az ügyfélszolgálattal. |

### 4. Jelenlegi üzleti folyamatok modellje
A mai képmegosztó platformok sok esetben nem felelnek meg a felhasználók egyszerűség és használhatóság iránti igényeinek. Gyakran túl sok funkcióval rendelkeznek, amelyek elvonják a figyelmet a lényegi tartalomtól. Nincs olyan platform, amely egyszerűen használható, letisztult felülettel rendelkezik, és a közösségi interakciókra helyezi a hangsúlyt.

### 5. Igényelt üzleti folyamatok modellje
A Best Gallery célja egy olyan képmegosztó platform létrehozása, amely egyszerű és felhasználóbarát. A felhasználók könnyedén tölthetnek fel és oszthatnak meg képeket, felfedezhetik mások alkotásait, és interakcióba léphetnek egymással. Az alkalmazás támogatja a kategóriákat és címkéket, amelyek megkönnyítik a tartalmak rendszerezését és keresését. A reszponzív dizájn biztosítja, hogy az alkalmazás minden eszközön jól használható legyen.

### 6. Használati esetek
**Felhasználó:**
- Regisztráció és bejelentkezés
- Profil szerkesztése
- Képek feltöltése és törlése
- Képek böngészése és keresése
- Kedvencek kezelése
- Üzenetküldés más felhasználóknak
- Jelszó módosítása és elfelejtett jelszó kezelése

**Adminisztrátor:**
- Felhasználók és tartalmak felügyelete
- Kategóriák és címkék kezelése
- Rendszerkarbantartás

### 7. Megfeleltetés, hogyan fedik le a használati esetek a követelményeket

| Használati eset | Követelmény(ek) |
|------------------|-------------------|
| Regisztráció | K1 |
| Bejelentkezés | K2 |
| Profil szerkesztése | K3 |
| Képek feltöltése és törlése | K4, K6 |
| Képek böngészése és megtekintése | K5, K7 |
| Képek keresése | K7 |
| Felhasználók keresése | K8 |
| Üzenetküldés | K9 |
| Kedvencek kezelése | K10 |
| Jelszó módosítása és elfelejtett jelszó | K11, K12 |
| Reszponzív dizájn | K13 |
| Segítség és támogatás | K14 |

### 8. Képernyőtervek
**Főoldal**
- **Elemek:** Legújabb és legnépszerűbb képek megjelenítése, keresőmező, navigációs menü

**Regisztrációs és bejelentkezési oldalak**
- **Elemek:** Regisztrációs űrlap (felhasználónév, email, jelszó), bejelentkezési űrlap (email, jelszó), elfelejtett jelszó link

**Profil oldal**
- **Elemek:** Profilkép, felhasználói adatok, feltöltött képek listája, profil szerkesztése gomb

**Kép feltöltési oldal**
- **Elemek:** Kép kiválasztása, cím, leírás, kategória, címkék megadása, feltöltés gomb

### 9. Forgatókönyv
**Forgatókönyv 1: Kép feltöltése**
1. A felhasználó bejelentkezik.
2. A navigációs menüben kiválasztja a "Kép feltöltése" opciót.
3. Kiválaszt egy képfájlt a számítógépéről.
4. Megadja a kép címét, leírását, kategóriáját és címkéit.
5. Rákattint a "Feltöltés" gombra.
6. A rendszer ellenőrzi a feltöltött fájlt és elmenti az adatbázisba.
7. A kép megjelenik a felhasználó profiljában és a főoldalon.

**Forgatókönyv 2: Kép keresése és kedvencekhez adása**
1. A felhasználó bejelentkezik.
2. A keresőmezőbe beír egy kulcsszót (pl. "tájkép").
3. A rendszer listázza a releváns képeket.
4. A felhasználó rákattint egy képre a részletek megtekintéséhez.
5. A képoldalon rákattint a "Kedvencekhez adás" gombra.
6. A kép hozzáadódik a felhasználó kedvenceihez.

### 10. Funkció - követelmény megfeleltetés

| Funkció | Követelmény(ek) |
|----------|------------------|
| Regisztráció | K1 |
| Bejelentkezés | K2 |
| Profil szerkesztése | K3 |
| Kép feltöltése | K4 |
| Képek megtekintése | K5 |
| Kép törlése | K6 |
| Képek keresése | K7 |
| Felhasználók keresése | K8 |
| Üzenetküldés | K9 |
| Kedvencek kezelése | K10 |
| Jelszó módosítása | K11 |
| Elfelejtett jelszó kezelése | K12 |
| Reszponzív dizájn | K13 |
| Segítség és támogatás | K14 |

### 11. Fogalomszótár
- **Profil**: A felhasználó személyes oldala az alkalmazásban.
- **Címke (Tag)**: Kulcsszó a képek kategorizálásához és kereséséhez.
- **Kedvencek**: A felhasználó által kedvelt képek gyűjteménye.
- **Üzenet**: Privát kommunikáció a felhasználók között.
- **Reszponzív dizájn**: Olyan webes kialakítás, amely alkalmazkodik a különböző eszközök képernyőméretéhez.
- **Kategória**: A képek főbb témakörök szerinti csoportosítása.
- **Elfelejtett jelszó**: Funkció a jelszó visszaállításához.

