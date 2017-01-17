import psycopg2

def get_pgc():
	pgc = psycopg2.connect("dbname='gps'")
	return pgc