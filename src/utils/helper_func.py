def convert_sqlite3rows_to_dict(sqlite3rows):
	if type(sqlite3rows) == list:
		res = []
		
		for row in sqlite3rows:
			res.append(dict(zip(row.keys(), row)))

		return res      
	
	return dict(zip(sqlite3rows.keys(), sqlite3rows))
