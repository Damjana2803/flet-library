# Flet Athena

Application built in [Flet](https://flet.dev) where students can schedule study meetups in Serbian language.

### How to run?

(optionally) Create a virtual enviorment (.venv) and activate it
```sh
python -m venv .venv

# Windows #
# in cmd.exe
.venv\Scripts\activate.bat
# in PowerShell
.venv\Scripts\Activate.ps1

# MacOS and Linux #
source .venv/bin/activate
```

Install pip packages
```sh
pip install -r "requirements.txt"
```

Move contents of `.env.example` to `.env`

Run flet app 
```sh
flet run main.py
```

Admin creds: 
| Field |  Value  | 
|:-----|:--------:|
| email | `admin@athena.com` |
|password   |  `admin`  |
