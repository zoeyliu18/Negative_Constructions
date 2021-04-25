from childespy import *
import pandas as pd 
import argparse, os


eng_uk = ['Belfast', 'Cruttenden', 'Fletcher', 'Forrester', 'Gathburn', 'Howe', 'Korman', 'Lara', 'MPI-EVA-Manchester', 'Manchester', 'Nuffield', 'Thomas', 'Tommerdahl', 'Wells']

eng_na = ['Bates', 'Bernstein', 'Bliss', 'Bloom', 'Bohannon', 'Braunwald', 'Brent', 'Brown', 'Clark', 'ComptonPater', 'Davis', 'Davis-CDI', 'Demetras1', 'Demetras2', 'Evans', 'Feldman', 'Garvey', 'Gathercole', 'Gelman', 'Gleason', 'Goad', 'Gopnik', 'HSLLD', 'Haggerty', 'Hall', 'Hicks', 'Higginson', 'Inkelas', 'Kuczaj', 'MacWhinney', 'McCune', 'McMillan', 'Menn', 'Morisset', 'Nelson', 'NewEngland', 'NewmanRatner', 'Penney', 'Peters', 'PetersonMcCabe', 'Post', 'Providence', 'Rollins', 'Sachs', 'Sawyer', 'Snow', 'Soderstrom', 'Sprott', 'Suppes', 'Tardif', 'Valian', 'VanHouten', 'VanKleeck', 'Warren', 'Weist']

#print(sorted(eng_uk))

#print(sorted(eng_na))

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--path', type = str, help = 'path for extracted childes_db data')

	args = parser.parse_args()

	path = args.path

	exist = []

	for file in os.listdir(path):
		if file.endswith('.csv'):
			file = file.split('.')[0]
			exist.append(file)

	
	for corpus in eng_uk:
		if corpus not in exist:
			print(corpus)
			data = get_utterances(corpus = corpus)
			data.to_csv(path + corpus + '.csv', encoding = 'utf-8')

	for corpus in eng_na:
		if corpus not in exist:
			print(corpus)
			data = get_utterances(corpus = corpus)
			data.to_csv(path + corpus + '.csv', encoding = 'utf-8')

