from src.scrapper import scrapper

sc = scrapper()
db = sc.collect()
db.to_csv('data/place_emploi_public.csv', index=False)
