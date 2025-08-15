# Bibliotečka Aplikacija

Aplikacija za upravljanje bibliotečkim fondom napisana u Python Flet framework-u.

## Opis aplikacije

Ova aplikacija omogućava upravljanje bibliotečkim fondom sa sledećim funkcionalnostima:

### Za administratore:
- **Upravljanje knjigama**: Dodavanje, uređivanje i brisanje knjiga iz fonda
- **Upravljanje članovima**: Registracija novih članova i upravljanje članarinama
- **Iznajmljivanje**: Praćenje iznajmljenih knjiga i proces vraćanja
- **Statistike**: Pregled najtraženijih knjiga i evidencija članarina

### Za članove:
- **Pretraga knjiga**: Pretraga bibliotečkog fonda po različitim kriterijumima
- **Rezervacije**: Rezervisanje knjiga koje su trenutno nedostupne
- **Moje knjige**: Pregled trenutno iznajmljenih knjiga
- **Profil**: Upravljanje ličnim podacima

## Tehnologije

- **Python 3.8+**
- **Flet** - UI framework
- **SQLite** - baza podataka
- **flet-navigator** - navigacija

## Instalacija

1. Klonirajte repozitorijum:
```bash
git clone <repository-url>
cd flet-library
```

2. Instalirajte potrebne pakete:
```bash
pip install -r requirements.txt
```

3. Pokrenite aplikaciju:
```bash
python src/main.py
```

## Struktura projekta

```
src/
├── components/          # UI komponente
├── controllers/         # Kontroleri za logiku
├── models/             # Modeli podataka
├── utils/              # Pomoćne funkcije
├── views/              # View-ovi aplikacije
│   ├── admin/          # Admin view-ovi
│   └── meets/          # Legacy view-ovi
└── main.py             # Glavna aplikacija
```

## Funkcionalnosti

### Autentifikacija
- **Admin prijava**: `admin@biblioteka.rs` / `admin123`
- **Član prijava**: `petar@email.com` / `member123`

### Modeli podataka
- **Book**: Knjige sa svim potrebnim podacima
- **Member**: Članovi biblioteke
- **Loan**: Iznajmljivanje knjiga
- **Reservation**: Rezervacije knjiga
- **Admin**: Administratori sistema

### Navigacija
- **Admin navigacija**: Dashboard, Knjige, Članovi, Iznajmljivanje, Statistike
- **Član navigacija**: Dashboard, Pretraga, Moje knjige, Rezervacije, Profil

## Razvoj

### Dodavanje novih funkcionalnosti
1. Kreirajte model u `models/` direktorijumu
2. Dodajte kontroler u `controllers/` direktorijumu
3. Kreirajte view u `views/` direktorijumu
4. Dodajte rutu u `main.py`

### Stilizacija
- Koristite `ResponsiveCard` za kartice
- Koristite `SnackBar` za obaveštenja
- Koristite `Loader` za učitavanje

## Licenca

MIT License
