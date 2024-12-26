def convert_sqlite3rows_to_dict(sqlite3rows):
	if type(sqlite3rows) == list:
		res = []
		
		for row in sqlite3rows:
			res.append(dict(zip(row.keys(), row)))

		return res      
	
	return dict(zip(sqlite3rows.keys(), sqlite3rows))

def faculties_options():
	import flet as ft
	
	return [
		ft.dropdown.Option('Ekonomski fakultet'),
		ft.dropdown.Option('Medicinski fakultet'),
		ft.dropdown.Option('Poljoprivredni fakultet'),
		ft.dropdown.Option('Pravni fakultet'),
		ft.dropdown.Option('Prirodno-matematički fakultet'),
		ft.dropdown.Option('Učiteljski fakultet'),
		ft.dropdown.Option('Fakultet za sport i fizičko vaspitanje'),
		ft.dropdown.Option('Fakultet tehničkih nauka'),
		ft.dropdown.Option('Filozofski fakultet'),
	]