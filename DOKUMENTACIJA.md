# Dokumentacija - Bibliotečka Aplikacija

## 1. Uvod

### 1.1 Opis projekta
Bibliotečka aplikacija je mobilna aplikacija napisana u Python Flet framework-u koja omogućava upravljanje bibliotečkim fondom. Aplikacija je namenjena bibliotekama za praćenje knjiga, članova, iznajmljivanja i rezervacija.

### 1.2 Ciljevi projekta
- Omogućiti administrativno upravljanje bibliotečkim fondom
- Pružiti članovima mogućnost pretrage i rezervacije knjiga
- Automatizovati proces iznajmljivanja i vraćanja knjiga
- Generisati statistike i izveštaje o aktivnostima

### 1.3 Tehnologije
- **Python 3.8+** - glavni programski jezik
- **Flet** - UI framework za kreiranje mobilnih aplikacija
- **SQLite** - baza podataka
- **flet-navigator** - navigacija između stranica

## 2. Arhitektura aplikacije

### 2.1 Struktura projekta
```
src/
├── components/          # UI komponente
│   ├── navbar.py       # Navigaciona traka
│   ├── snack_bar.py    # Obaveštenja
│   ├── loader.py       # Komponenta za učitavanje
│   └── responsive_card.py # Responzivne kartice
├── controllers/         # Kontroleri za logiku
│   ├── login_controller.py # Kontroler za prijavu
│   └── register_controller.py # Kontroler za registraciju
├── models/             # Modeli podataka
│   ├── book.py         # Model knjige
│   ├── member.py       # Model člana
│   ├── loan.py         # Model iznajmljivanja
│   ├── reservation.py  # Model rezervacije
│   └── user.py         # Model korisnika (admin)
├── utils/              # Pomoćne funkcije
│   ├── db.py           # Baza podataka
│   ├── global_state.py # Globalno stanje
│   ├── route_guard.py  # Zaštita ruta
│   └── validators.py   # Validacija podataka
├── views/              # View-ovi aplikacije
│   ├── admin/          # Admin view-ovi
│   │   ├── admin_dashboard.py # Admin dashboard
│   │   ├── admin_books.py # Upravljanje knjigama
│   │   └── admin_statistics.py # Statistike
│   ├── login_view.py   # Prijava
│   ├── register_view.py # Registracija
│   ├── member_dashboard.py # Članovski dashboard
│   ├── book_search.py  # Pretraga knjiga
│   ├── my_loans.py     # Moje iznajmljene knjige
│   ├── my_reservations.py # Moje rezervacije
│   └── member_profile.py # Profil člana
└── main.py             # Glavna aplikacija
```

### 2.2 Modeli podataka

#### 2.2.1 Book (Knjiga)
```python
@dataclass
class Book:
    id: Optional[int] = None
    title: str = ""           # Naslov knjige
    author: str = ""          # Autor
    isbn: str = ""           # ISBN broj
    category: str = ""       # Kategorija
    publication_year: int = 0 # Godina izdanja
    publisher: str = ""      # Izdavač
    description: str = ""    # Opis
    total_copies: int = 1    # Ukupan broj primeraka
    available_copies: int = 1 # Dostupni primerci
    location: str = ""       # Lokacija u biblioteci
    status: str = "available" # Status (available, unavailable, maintenance)
```

#### 2.2.2 Member (Član)
```python
@dataclass
class Member:
    id: Optional[int] = None
    first_name: str = ""     # Ime
    last_name: str = ""      # Prezime
    email: str = ""          # E-adresa
    phone: str = ""          # Telefon
    address: str = ""        # Adresa
    membership_number: str = "" # Broj članstva
    membership_type: str = "regular" # Tip članstva (regular, student, senior)
    membership_status: str = "active" # Status članstva
    max_loans: int = 5       # Maksimalan broj iznajmljivanja
    current_loans: int = 0   # Trenutno iznajmljeno
```

#### 2.2.3 Loan (Iznajmljivanje)
```python
@dataclass
class Loan:
    id: Optional[int] = None
    book_id: int = 0         # ID knjige
    member_id: int = 0       # ID člana
    loan_date: datetime = None # Datum iznajmljivanja
    due_date: datetime = None # Datum vraćanja
    return_date: datetime = None # Datum stvarnog vraćanja
    status: str = "active"   # Status (active, returned, overdue, lost)
    fine_amount: float = 0.0 # Iznos kazne
```

#### 2.2.4 Reservation (Rezervacija)
```python
@dataclass
class Reservation:
    id: Optional[int] = None
    book_id: int = 0         # ID knjige
    member_id: int = 0       # ID člana
    reservation_date: datetime = None # Datum rezervacije
    expiry_date: datetime = None # Datum isteka rezervacije
    status: str = "active"   # Status (active, fulfilled, expired, cancelled)
    priority: int = 1        # Prioritet rezervacije
```

## 3. Funkcionalnosti

### 3.1 Autentifikacija i autorizacija

#### 3.1.1 Prijava
- Podržava prijavu za administratore i članove
- Admin prijava: `admin@biblioteka.rs` / `admin123`
- Član prijava: `petar@email.com` / `member123`
- Validacija podataka i obaveštenja o greškama

#### 3.1.2 Registracija članova
- Forma za registraciju novih članova
- Validacija svih polja (ime, prezime, email, telefon, adresa)
- Izbor tipa članstva (redovno, studentsko, penzionersko)

### 3.2 Admin funkcionalnosti

#### 3.2.1 Admin Dashboard
- Pregled ključnih statistika (ukupno knjiga, članova, iznajmljenih)
- Brzi pristup glavnim funkcionalnostima
- Navigacija ka svim admin sekcijama

#### 3.2.2 Upravljanje knjigama
- **Dodavanje novih knjiga**: Forma sa svim potrebnim poljima
- **Uređivanje knjiga**: Izmena postojećih podataka
- **Brisanje knjiga**: Sa potvrdom brisanja
- **Pretraga knjiga**: Po naslovu, autoru, ISBN-u
- **Pregled stanja**: Dostupnost i lokacija primeraka

#### 3.2.3 Statistike
- **Najtraženije knjige**: Lista knjiga sa brojem iznajmljivanja
- **Distribucija članstva**: Po tipovima članstva
- **Mesečni trendovi**: Grafikon aktivnosti
- **Izveštaji**: Mogućnost preuzimanja izveštaja

### 3.3 Član funkcionalnosti

#### 3.3.1 Članovski Dashboard
- Pregled ličnih podataka i aktivnosti
- Statistike iznajmljivanja i rezervacija
- Brzi pristup glavnim funkcionalnostima

#### 3.3.2 Pretraga knjiga
- **Pretraga po tekstu**: Naslov, autor, ISBN
- **Filtriranje**: Po kategoriji i dostupnosti
- **Detalji knjige**: Kompletne informacije o knjizi
- **Iznajmljivanje/rezervacija**: Direktno iz rezultata pretrage

#### 3.3.3 Moje iznajmljene knjige
- **Lista iznajmljenih knjiga**: Sa datumima i statusom
- **Produžavanje**: Mogućnost produžavanja roka
- **Vraćanje**: Označavanje knjiga kao vraćene
- **Kazne**: Pregled i plaćanje kazni za prekoračenja

#### 3.3.4 Moje rezervacije
- **Aktivne rezervacije**: Sa datumima isteka
- **Istorija rezervacija**: Ispunjene i otkazane
- **Otkazivanje**: Mogućnost otkazivanja rezervacija
- **Produžavanje**: Produžavanje roka rezervacije

#### 3.3.5 Profil člana
- **Lični podaci**: Pregled i uređivanje
- **Informacije o članstvu**: Status, tip, datumi
- **Promena lozinke**: Sigurna promena lozinke
- **Istorija aktivnosti**: Preuzimanje istorije

## 4. Korisnički interfejs

### 4.1 Navigacija
- **Admin navigacija**: Dashboard, Knjige, Članovi, Iznajmljivanje, Statistike
- **Član navigacija**: Dashboard, Pretraga, Moje knjige, Rezervacije, Profil
- **Responzivni dizajn**: Prilagođen različitim veličinama ekrana

### 4.2 Komponente
- **ResponsiveCard**: Kartice za brzi pristup funkcionalnostima
- **SnackBar**: Obaveštenja o uspešnim akcijama i greškama
- **Loader**: Indikator učitavanja tokom operacija
- **Dialog**: Modalni prozori za forme i potvrde

### 4.3 Stilizacija
- **Konzistentan dizajn**: Jedinstveni vizuelni identitet
- **Boje**: Plava tema sa akcentnim bojama za status
- **Tipografija**: Čitljivost i hijerarhija informacija
- **Ikone**: Intuitivne ikone za sve akcije

## 5. Baza podataka

### 5.1 SQLite baza
- **Lokalna baza**: SQLite za jednostavnost
- **Tabele**: books, members, loans, reservations, admins
- **Relacije**: Foreign keys za povezivanje podataka
- **Indeksi**: Za brzu pretragu i sortiranje

### 5.2 Skripta za inicijalizaciju
```python
def db_init():
    # Kreiranje tabela ako ne postoje
    # Inicijalno popunjavanje sa test podacima
    # Kreiranje admin korisnika
```

## 6. Sigurnost

### 6.1 Autentifikacija
- **Hashiranje lozinki**: Sigurno čuvanje lozinki
- **Sesije**: Upravljanje korisničkim sesijama
- **Route guards**: Zaštita pristupa stranicama

### 6.2 Validacija
- **Input validacija**: Provera svih korisničkih unosa
- **SQL injection protection**: Sigurni upiti ka bazi
- **XSS protection**: Zaštita od cross-site scripting

## 7. Testiranje

### 7.1 Jedinični testovi
- **Modeli**: Testiranje modela podataka
- **Kontroleri**: Testiranje poslovne logike
- **Validacija**: Testiranje validacije podataka

### 7.2 Integracioni testovi
- **UI testovi**: Testiranje korisničkog interfejsa
- **Baza podataka**: Testiranje CRUD operacija
- **Navigacija**: Testiranje ruta i navigacije

## 8. Deployment

### 8.1 Lokalno pokretanje
```bash
# Instalacija zavisnosti
pip install -r requirements.txt

# Pokretanje aplikacije
python src/main.py
```

### 8.2 Mobilna aplikacija
```bash
# Kreiranje APK fajla
flet build apk

# Kreiranje iOS aplikacije
flet build ios
```

### 8.3 Desktop aplikacija
```bash
# Kreiranje desktop aplikacije
flet build windows
flet build macos
flet build linux
```

## 9. Održavanje i razvoj

### 9.1 Verzioniranje
- **Semantic versioning**: MAJOR.MINOR.PATCH
- **Git workflow**: Feature branches i pull requests
- **Changelog**: Praćenje promena

### 9.2 Dokumentacija
- **Kod dokumentacija**: Docstrings za sve funkcije
- **API dokumentacija**: Opis svih endpoint-ova
- **Korisnička dokumentacija**: Uputstvo za korišćenje

### 9.3 Monitoring
- **Logging**: Praćenje grešaka i aktivnosti
- **Performance monitoring**: Praćenje performansi
- **User analytics**: Analiza korišćenja

## 10. Zaključak

Bibliotečka aplikacija predstavlja kompletan sistem za upravljanje bibliotečkim fondom koji omogućava:

1. **Efikasno upravljanje**: Administrativno upravljanje knjigama i članovima
2. **Korisničko iskustvo**: Intuitivan interfejs za članove
3. **Automatizaciju**: Automatsko praćenje iznajmljivanja i kazni
4. **Analitiku**: Detaljne statistike i izveštaje
5. **Skalabilnost**: Mogućnost proširenja funkcionalnosti

Aplikacija je napisana koristeći moderne Python tehnologije i prati najbolje prakse u razvoju softvera. Dizajn je responzivan i prilagođen različitim uređajima, dok je arhitektura modularna i laka za održavanje.

### 10.1 Budući razvoj
- **Online baza podataka**: Migracija na PostgreSQL ili MySQL
- **Push notifikacije**: Obaveštenja o isteku roka
- **QR kod skeniranje**: Brzo iznajmljivanje/vraćanje
- **E-knjige**: Podrška za digitalne knjige
- **API**: REST API za integraciju sa drugim sistemima


