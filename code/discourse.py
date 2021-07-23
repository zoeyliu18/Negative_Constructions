import io, os, argparse
import pandas as pd

AUX = ['can', 'could', 'ca', 'dare', 'do', 'did', 'does', 'have', 'had', 'has', 'may', 'might', 'must', 'need', 'ought', 'shall', 'should', 'will', 'would']
COP = ['be', 'is', 'was', 'am', 'are', 'were']
SUBJ = ['I', 'you', 'she', 'he', 'they', 'it', 'we']
POSS = ['my', 'mine', 'your', 'yours', 'her', 'hers', 'his', 'their', 'theirs', 'its', 'us', 'ours']


#### Selected children for investigating individual variation ####

individuals = {'MacWhinney': ['Ross'], 'Davis': ['Rebecca', 'Cameron', 'Georgia', 'Rowan', 'Hannah'], 'Tardif': ['Julia', 'Melissa'], 'Wells': ['Elspeth', 'Gary', 'Gavin', 'Ellen', 'Jason', 'Rosie', 'Benjamin', 'Darren', 'Nancy', 'Penny', 'Debbie'], 'Braunwald': ['Laura'],
			   'Providence': ['William', 'Lily', 'Naima', 'Ethan', 'Alex'], 'Howe': ['Oliver', 'Sally'], 'Bloom': ['Peter'],
			   'Manchester': ['John', 'Carl', 'Liz', 'Warren', 'Joel', 'Gail', 'Dominic', 'Anne'], 'Brown': ['Eve'], 'Nelson': ['Emily'], 'Lara': ['Lara'],
			   'NewmanRatner': ['6510LC', '5196AVI24', '5266EC', '5346GG24mos', '5949DL24mos', '4724LM24mos', '4946RC', '7075MB24mos', '7534EM24mos'],
			   'Peters': ['Seth'], 'Post': ['Tow', 'Lew', 'She'], 'Bates': ['Keith', 'Gloria', 'Amy', 'Mandy', 'Hank'], 'McCune': ['Alice'], 'MPI-EVA-Manchester': ['Eleanor', 'Fraser'],
			   'Sachs': ['Naomi'], 'Suppes': ['Nina'], 'Demetras1': ['Trevor'], 'McCune': ['Alice', 'Jase'], 'Feldman': ['Steven'], 'Weist': ['Roman', 'Jillian'],
			   'Kuczaj': ['Abe'], 'Demetras2': ['Michael', 'Jimmy'], 'Cruttenden': ['Lucy']}

### reading in sentences in CoNLL format ###

def conll_read_sentence(file_handle):
	sent = []
	for line in file_handle:
		line = line.strip('\n')
		if line.startswith('#') is False:
			toks = line.split("\t")
			if len(toks) != 10 and sent not in [[], ['']]:
				return sent 
			if len(toks) == 10 and '-' not in toks[0] and '.' not in toks[0]:
				sent.append(toks)	
	return None

### get descriptive statistics of age for all children ###

def descriptive(directory):

	child_data = {}
	parent_data = {}

	age_list = []
	
	child_raw = []
	parent_raw = []

	for file in os.listdir(directory):
		if file.endswith('.conllu'):
			with io.open(directory + file, encoding = 'utf-8') as f:
				sent = conll_read_sentence(f)

				while sent is not None:
					speaker_info = sent[0][-2].split()
					corpus_info = sent[0][-1].split()

					if speaker_info[-1] in ['Mother', 'Father', 'Target_Child', 'Child']:
						speaker_name = speaker_info[0]
						speaker_role = speaker_info[-1]

						child_name = corpus_info[0]

						age = ''
						
						try:
							age = int(float(corpus_info[1]))
						except:
							age = ''

						if age != '':

							corpus_name = file.split('.')[0]

							age_list.append(str(age))

							info = [str(age), corpus_name + child_name]

							if speaker_role in ['Target_Child', 'Child']:
								child_raw.append(info)

							if speaker_role in ['Mother', 'Father']:
								parent_raw.append(info)

					sent = conll_read_sentence(f)

	age_list = set(age_list)

	for age in age_list:
	
		child_c = []
		child_u = 0
		parent_c = []
		parent_u = 0

		for tok in child_raw:
			if tok[0] == age:
				if tok[1] not in child_c:
					child_c.append(tok[1])

				child_u += 1

		for tok in parent_raw:
			if tok[0] == age:
				if tok[1] not in parent_c:
					parent_c.append(tok[1])

				parent_u += 1

		child_data[age] = [len(set(child_c)), child_u]
		parent_data[age] = [len(set(parent_c)), parent_u]

	return child_data, parent_data


### get descriptive statistics of uttrance length for all children ###

def uttrance_len(directory):

	child_data = {}
	parent_data = {}

	ul_list = []
	
	child_raw = []
	parent_raw = []

	for file in os.listdir(directory):
		if file.endswith('.conllu'):
			with io.open(directory + file, encoding = 'utf-8') as f:
				sent = conll_read_sentence(f)

				while sent is not None:
					speaker_info = sent[0][-2].split()
					corpus_info = sent[0][-1].split()

					if speaker_info[-1] in ['Mother', 'Father', 'Target_Child', 'Child']:
						speaker_name = speaker_info[0]
						speaker_role = speaker_info[-1]

						child_name = corpus_info[0]

						age = ''

						try:
							age = int(float(corpus_info[1]))
						except:
							age = ''

						if age != '' and age >= 12 and age <= 72:

							ul = len(sent)

							corpus_name = file.split('.')[0]

							ul_list.append(str(ul))

							info = [str(ul), corpus_name + child_name]

							if speaker_role in ['Target_Child', 'Child']:
								child_raw.append(info)

							if speaker_role in ['Mother', 'Father']:
								parent_raw.append(info)

					sent = conll_read_sentence(f)

	ul_list = set(ul_list)

	for ul in ul_list:
	
		child_c = []
		child_u = 0
		parent_c = []
		parent_u = 0

		for tok in child_raw:
			if tok[0] == ul:
				if tok[1] not in child_c:
					child_c.append(tok[1])

				child_u += 1

		for tok in parent_raw:
			if tok[0] == ul:
				if tok[1] not in parent_c:
					parent_c.append(tok[1])

				parent_u += 1

		child_data[ul] = [len(set(child_c)), child_u]
		parent_data[ul] = [len(set(parent_c)), parent_u]

	return child_data, parent_data


### get descriptive statistics of individual child ###

def individual_descriptive(file, name):

	child_data = {}
	parent_data = {}

	age_list = []
	
	child_raw = []
	parent_raw = []

	with io.open(file, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)

		while sent is not None:
			speaker_info = sent[0][-2].split()
			corpus_info = sent[0][-1].split()

			if speaker_info[-1] in ['Mother', 'Father', 'Target_Child', 'Child']:
				speaker_name = speaker_info[0]
				speaker_role = speaker_info[-1]

				child_name = corpus_info[0]
				try:
					age = int(float(corpus_info[1]))
				except:
					age = ''

				if age != '' and child_name == name:

					corpus_name = file.split('.')[0]

					age_list.append(str(age))

					info = [str(age), corpus_name + child_name]

					if speaker_role in ['Target_Child', 'Child']:
						child_raw.append(info)

					if speaker_role in ['Mother', 'Father']:
						parent_raw.append(info)

			sent = conll_read_sentence(f)

	age_list = set(age_list)

	for age in age_list:
	
		child_c = []
		child_u = 0
		parent_c = []
		parent_u = 0

		for tok in child_raw:
			if tok[0] == age:
				if tok[1] not in child_c:
					child_c.append(tok[1])

				child_u += 1

		for tok in parent_raw:
			if tok[0] == age:
				if tok[1] not in parent_c:
					parent_c.append(tok[1])

				parent_u += 1

		child_data[age] = [len(set(child_c)), child_u]
		parent_data[age] = [len(set(parent_c)), parent_u]

	return child_data, parent_data


### dependents ###

def dependents(index, sent):

	idx_list = []
	d_list = []

	for d in sent:
		if int(d[6]) == int(index):
			idx_list.append(int(d[0]))

	idx_list.sort()

	for idx in idx_list:
		d_list.append(sent[idx - 1])

	return d_list


### has negation marker as dependent? ###

def has_neg(index, sent):

	neg_d = []

	d_list = dependents(index, sent)

	for d in d_list:
		if d[1] in ['not', 'no', "n't"] and d[7] not in ['discourse']:	
			neg_d.append(d)

		if d[2] in ['more']:
			d_d_list = dependents(d[0], sent)

			for z in d_d_list:
				if z[1] in ['not', 'no', "n't"]:
					neg_d.append(z)

	return neg_d


### get negation and auxiliaries of a verb if there are any ###

def neg_verb(tok, sent):

	aux = 'NONE'
	aux_stem = 'NONE'
	aux_idx = ''

	neg = ''

	try:
		potential = sent[int(tok[0]) - 2]

		if potential[1] in ['not', 'no', "n't"]:
			neg = potential

			try:
				aux_tok = sent[int(tok[0]) - 3]
				if aux_tok[3] == 'AUX': 
					aux = aux_tok[1]
					aux_stem = aux_tok[2]
					aux_idx = aux_tok[0]

			except:
				aux = 'NONE'

		elif potential[1] not in ['not', 'no', "n't"] and potential[1].endswith("n't"):
			neg = [potential[0], "n't"]
							
			aux = potential[1][ : -3]
			aux_stem = potential[1][ : -3]
			aux_id = potential[0]

	except:
						
		try:
			far = sent[int(tok[0]) - 3] 
						
			if far[1] in ['not', 'no', "n't"]:
				neg = far
						
			if far[1].endswith("n't"):
				neg = far

				aux = far[1][ : -3]
				aux_stem = aux
				aux_id = far[0]

		except:
			try:
				temp = has_neg(tok[0], sent)
				if len(temp) != 0:
					neg = temp[-1]

					try:
						aux_tok = sent[int(neg[0]) - 2]
						
						if aux_tok[3] == 'AUX': 
							aux = aux_tok[1]
							aux_stem = aux_tok[2]
							aux_idx = aux_tok[0]

					except:
						aux = 'NONE'

			except:
				neg = ''

	return neg, aux, aux_stem, aux_idx

### get previous utterance(s) ###

def context(index, all_sentences):

	current = all_sentences[index]
	previous = ''

	if current[0][1] in ['no', 'not', "n't"] and current[0][7] == 'discourse':
		child_info = current[0][-1].split()
		target_child_name = child_info[0]
		target_child_id = child_info[-2]
		transcript_id = child_info[-1]
		speaker_role = current[0][-2].split()[-1]

		try:
			previous = all_sentences[index - 1]

		except:
			previous = ''
	
	if previous != '':
		previous_child_info = previous[0][-1].split()
		previous_target_child_name = child_info[0]
		previous_target_child_id = child_info[-2]
		previous_transcript_id = child_info[-1]
		previous_speaker_role = previous[0][-2].split()[-1]

		if previous_target_child_name == target_child_name and previous_target_child_id == target_child_id and  previous_transcript_id == transcript_id:
			if speaker_role in ['Target_Child'] and previous_speaker_role in ['Mother', 'Father']:
				previous = previous 
			if speaker_role in ['Mother', 'Father'] and previous_speaker_role in ['Target_Child']:
				previous = previous 
			if speaker_role in ['Target_Child'] and previous_speaker_role in ['Target_Child']:
				previous = previous 

		return previous, previous_speaker_role
	else:
		return 'Nothing', 'Nothing'


### Get all data from corpus *.conllu file ###

def get_data(file):

	all_data = []

	with io.open(file, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)

		while sent is not None:
			all_data.append(sent)

			sent = conll_read_sentence(f)

	return all_data


### emotion: rejection ###


def emotion(index, sent, corpus_name, level, data):

	function = 'rejection'

	saying = ' '.join(w[1] for w in sent)
		
	speaker_info = sent[0][-2].split()
	corpus_info = sent[0][-1].split()

	speaker_name = speaker_info[0]
	speaker_role = speaker_info[-1]

	child_name = corpus_info[0]

	sent_type = corpus_info[3]

	age = ''

	try:
		age = int(float(corpus_info[1]))

	except:
		age = ''
				
	if age != '' and age >= 12 and age <= 72 and speaker_role in ['Target_Child', 'Child', 'Mother', 'Father'] and level == 's':

		for tok in sent:

			if tok[2] in ['like', 'want', 'wan'] or tok[1] in ['like', 'likes', 'liked', 'want', 'wants', 'wanted', 'wanna', 'wanna'] and tok[3] == 'VERB':  

				info = ''

				### include cases such as 'I don't like book' ###

				neg, aux, aux_stem, aux_idx = neg_verb(tok, sent)

				subj = 'NONE'
				subj_stem = 'NONE'
				subj_idx = ''

				d_list = dependents(tok[0], sent)

				for d in d_list:
					if d[3] == 'AUX' or d[7] == 'aux':
						aux = d[1]
						aux_stem = d[2]
						aux_idx = d[0]

				for d in d_list:			
					if d[7] == 'nsubj':								
						subj = d[1]
						subj_stem = d[2]
						subj_idx = d[0]

				if neg != '':
					info = ['emotion', function, tok[2], neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative', 'sentential']

				else:
					info = ['emotion', function, tok[2], '', aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'positive', 'sentential']

				if info != '':
					return info

	if age != '' and age >= 12 and age <= 72 and speaker_role in ['Target_Child', 'Child', 'Mother', 'Father'] and level == 'd':
		previous, previous_speaker_role = context(index, data)
	
		if previous != 'Nothing':

			previous_saying = [tok[1] for tok in previous]
			previous_saying = ' '.join(w for w in previous_saying)
			previous_sent_type = previous[0][-1].split()[3]

			for tok in previous:

				if (tok[2] in ['like', 'want', 'wan'] or tok[1] in ['like', 'likes', 'liked', 'want', 'wants', 'wanted', 'wanna', 'wanna']) and tok[3] == 'VERB':  

					info = ''

					neg, aux, aux_stem, aux_idx = neg_verb(tok, previous)

					subj = 'NONE'
					subj_stem = 'NONE'
					subj_idx = ''

					d_list = dependents(tok[0], previous)

					for d in d_list:
						if d[3] == 'AUX' or d[7] == 'aux':
							aux = d[1]
							aux_stem = d[2]
							aux_idx = d[0]

					for d in d_list:			
						if d[7] == 'nsubj':								
							subj = d[1]
							subj_stem = d[2]
							subj_idx = d[0]

					if neg != '':
						info = ['emotion', function, tok[2], neg[1], aux, aux_stem, subj, subj_stem, age, previous_speaker_role, speaker_role, previous_saying, saying, len(previous), len(sent), previous_sent_type, sent_type, corpus_name + ' ' + child_name, 'negative', 'discourse']

					else:
						info = ['emotion', function, tok[2], '', aux, aux_stem, subj, subj_stem, age, previous_speaker_role, speaker_role, previous_saying, saying, len(previous), len(sent), previous_sent_type, sent_type, corpus_name + ' ' + child_name, 'positive', 'discourse']

					if info != '':
						return info

	return None


### theory of mind: epistemic ###

def epistemic(index, sent, corpus_name, level, data):

	function = 'epistemic'
			
	saying = ' '.join(w[1] for w in sent)
		
	speaker_info = sent[0][-2].split()
	corpus_info = sent[0][-1].split()

	speaker_name = speaker_info[0]
	speaker_role = speaker_info[-1]

	child_name = corpus_info[0]

	sent_type = corpus_info[3]

	age = ''

	try:
		age = int(float(corpus_info[1]))

	except:
		age = ''

	if age != '' and age >= 12 and age <= 72 and speaker_role in ['Target_Child', 'Child', 'Mother', 'Father'] and level == 's':

		for tok in sent:

			if (tok[2] in ['know', 'think', 'remember'] or tok[1] in ['know', 'knows', 'knew', 'think', 'thinks', 'thought', 'remember', 'remembers', 'remembered']) and tok[3] == 'VERB': 

				info = ''

				neg, aux, aux_stem, aux_idx = neg_verb(tok, sent)

				subj = 'NONE'
				subj_stem = 'NONE'
				subj_idx = ''

				d_list = dependents(tok[0], sent)

				for d in d_list:
					if d[3] == 'AUX' or d[7] == 'aux':
						aux = d[1]
						aux_stem = d[2]
						aux_idx = d[0]				

					if d[7] == 'nsubj':								
						subj = d[1]
						subj_stem = d[2]
						subj_idx = d[0] 

				if neg != '':
					info = ['epistemic', function, tok[2], neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative', 'sentential']

				else:
					info = ['epistemic', function, tok[2], '', aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'positive', 'sentential']

				if info != '':
					return info
			
			if tok[2] in ['dunno', 'duno']:

				info = ''

				subj = 'NONE'
				subj_stem = 'NONE'
				subj_idx = ''

				d_list = dependents(tok[0], sent)

				for d in d_list:

					if d[7] == 'nsubj':								
						subj = d[1]
						subj_stem = d[2]
						subj_idx = d[0] 
				
				info = ['epistemic', function, 'know', "n't", 'dunno', 'do', subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative', 'sentential']

				if info != '':
					return info

	if age != '' and age >= 12 and age <= 72 and speaker_role in ['Target_Child', 'Child', 'Mother', 'Father'] and level == 'd':
		previous, previous_speaker_role = context(index, data)
	
		if previous != 'Nothing':

			previous_saying = [tok[1] for tok in previous]
			previous_saying = ' '.join(w for w in previous_saying)
			previous_sent_type = previous[0][-1].split()[3]

			for tok in previous:

				if (tok[2] in ['know', 'think', 'remember'] or tok[1] in ['know', 'knows', 'knew', 'think', 'thinks', 'thought', 'remember', 'remembers', 'remembered']) and tok[3] == 'VERB': 

					info = ''

					neg, aux, aux_stem, aux_idx = neg_verb(tok, previous)

					subj = 'NONE'
					subj_stem = 'NONE'
					subj_idx = ''

					d_list = dependents(tok[0], previous)

					for d in d_list:
						if d[3] == 'AUX' or d[7] == 'aux':
							aux = d[1]
							aux_stem = d[2]
							aux_idx = d[0]				

						if d[7] == 'nsubj':								
							subj = d[1]
							subj_stem = d[2]
							subj_idx = d[0] 

					if neg != '':
						info = ['epistemic', function, tok[2], neg[1], aux, aux_stem, subj, subj_stem, age, previous_speaker_role, speaker_role, previous_saying, saying, len(previous), len(sent), previous_sent_type, sent_type, corpus_name + ' ' + child_name, 'negative', 'discourse']

					else:
						info = ['epistemic', function, tok[2], '', aux, aux_stem, subj, subj_stem, age, previous_speaker_role, speaker_role, previous_saying, saying, len(previous), len(sent), previous_sent_type, sent_type, corpus_name + ' ' + child_name, 'positive', 'discourse']

					if info != '':
						return info
			
				if tok[2] in ['dunno', 'duno']:

					info = ''

					subj = 'NONE'
					subj_stem = 'NONE'
					subj_idx = ''

					d_list = dependents(tok[0], previous)

					for d in d_list:

						if d[7] == 'nsubj':								
							subj = d[1]
							subj_stem = d[2]
							subj_idx = d[0] 
				
					info = ['epistemic', function, 'know', "n't", 'dunno', 'do', subj, subj_stem, age, previous_speaker_role, speaker_role, previous_saying, saying, len(previous), len(sent), previous_sent_type, sent_type, corpus_name + ' ' + child_name, 'negative', 'discourse']

					if info != '':
						return info

	return None


### motor control ###

def motor(index, sent, corpus_name, level, data):

	function = 'epistemic'
			
	saying = ' '.join(w[1] for w in sent)
		
	speaker_info = sent[0][-2].split()
	corpus_info = sent[0][-1].split()

	speaker_name = speaker_info[0]
	speaker_role = speaker_info[-1]

	child_name = corpus_info[0]

	sent_type = corpus_info[3]

	age = ''

	try:
		age = int(float(corpus_info[1]))

	except:
		age = ''

	if age != '' and age >= 12 and age <= 72 and speaker_role in ['Target_Child', 'Child', 'Mother', 'Father'] and level == 's':

		for tok in sent:

			if tok[1] not in ['like', 'liked', 'likes', 'want', 'wanted', 'wants', 'know', 'knew', 'knows', 'think', 'thought', 'thinks', 'remember', 'remembered', 'remembers', 'have', 'has', 'had', 'dunno'] and tok[3] == 'VERB':

				info = ''

				d_list = dependents(tok[0], sent)

				subj = 'NONE'
				subj_stem = 'NONE'
				subj_idx = ''

				neg, aux, aux_stem, aux_idx = neg_verb(tok, sent)

				for d in d_list:
					if d[7] == 'nsubj':
						subj = d[1]
						subj_stem = d[2]
						subj_idx = d[0]

					if d[7] == 'aux':
						aux = d[1]
						aux_stem = d[2]
						aux_idx = d[0]

				if subj == 'NONE' and sent_type.startswith('imperative'):

					function = 'prohibition'
					
					if neg != '' and subj == 'NONE' and aux_stem == 'do':
						info = ['motor', function, tok[2], neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative', 'sentential']

					if neg == '' and subj == 'NONE':
						info = ['motor', function, tok[2], '', aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'positive', 'sentential']

				else:

					function = 'inability'

					if neg != '' and subj in ['I', 'i'] and aux_stem == 'can':
						info = ['motor', function, tok[2], neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative', 'sentential']

					if neg == '' and subj in ['I', 'i'] and aux_stem == 'can':
						info = ['motor', function, tok[2], '', aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'positive', 'sentential']

				if info != '':
					return info

	if age != '' and age >= 12 and age <= 72 and speaker_role in ['Target_Child', 'Child', 'Mother', 'Father'] and level == 'd':
		previous, previous_speaker_role = context(index, data)
	
		if previous != 'Nothing':

			previous_saying = [tok[1] for tok in previous]
			previous_saying = ' '.join(w for w in previous_saying)
			previous_sent_type = previous[0][-1].split()[3]

			for tok in previous:

				if tok[1] not in ['like', 'liked', 'likes', 'want', 'wanted', 'wants', 'know', 'knew', 'knows', 'think', 'thought', 'thinks', 'remember', 'remembered', 'remembers', 'have', 'has', 'had', 'dunno'] and tok[3] == 'VERB':

					info = ''

					d_list = dependents(tok[0], previous)

					subj = 'NONE'
					subj_stem = 'NONE'
					subj_idx = ''

					neg, aux, aux_stem, aux_idx = neg_verb(tok, previous)

					for d in d_list:
						if d[7] == 'nsubj':
							subj = d[1]
							subj_stem = d[2]
							subj_idx = d[0]

						if d[7] == 'aux':
							aux = d[1]
							aux_stem = d[2]
							aux_idx = d[0]

					if subj == 'NONE' and sent_type.startswith('imperative'):

						function = 'prohibition'
					
						if neg != '' and subj == 'NONE' and aux_stem == 'do':
							info = ['motor', function, tok[2], neg[1], aux, aux_stem, subj, subj_stem, age, previous_speaker_role, speaker_role, previous_saying, saying, len(previous), len(sent), previous_sent_type, sent_type, corpus_name + ' ' + child_name, 'negative', 'discourse']

						if neg == '' and subj == 'NONE':
							info = ['motor', function, tok[2], '', aux, aux_stem, subj, subj_stem, age, previous_speaker_role, speaker_role, previous_saying, saying, len(previous), len(sent), previous_sent_type, sent_type, corpus_name + ' ' + child_name, 'positive', 'discourse']

					else:

						function = 'inability'

						if neg != '' and subj in ['I', 'i'] and aux_stem == 'can':
							info = ['motor', function, tok[2], neg[1], aux, aux_stem, subj, subj_stem, age, previous_speaker_role, speaker_role, previous_saying, saying, len(previous), len(sent), previous_sent_type, sent_type, corpus_name + ' ' + child_name, 'negative', 'discourse']

						if neg == '' and subj in ['I', 'i'] and aux_stem == 'can':
							info = ['motor', function, tok[2], '', aux, aux_stem, subj, subj_stem, age, previous_speaker_role, speaker_role, previous_saying, saying, len(previous), len(sent), previous_sent_type, sent_type, corpus_name + ' ' + child_name, 'positive', 'discourse']

					if info != '':
						return info

	return None


### language learning: labeling ###

def learning(index, sent, corpus_name, level, data):

	function = 'labeling'
			
	saying = ' '.join(w[1] for w in sent)
		
	speaker_info = sent[0][-2].split()
	corpus_info = sent[0][-1].split()

	speaker_name = speaker_info[0]
	speaker_role = speaker_info[-1]

	child_name = corpus_info[0]

	sent_type = corpus_info[3]

	age = ''

	try:
		age = int(float(corpus_info[1]))

	except:
		age = ''

	if age != '' and age >= 12 and age <= 72 and speaker_role in ['Target_Child', 'Child', 'Mother', 'Father'] and level == 's':

		for tok in sent:

			if tok[2] in ['be'] or tok[1] in ['am', 'was', 'is', 'are', 'were', "'m", "'s", "re"]:

				info = ''
				neg = ''

				head = sent[int(tok[6]) - 1]

				pred = ''
				pred_stem = ''
				pred_pos = ''

				if head != '' and head[3] in ['NOUN', 'PROPN', 'PRON', 'ADJ'] and head[1] not in POSS:
					pred = head[1]
					pred_stem = head[2]
					pred_pos = head[3]

				expletive = ''

				d_list = dependents(tok[0], sent)

				for d in d_list:

					if d[7] == 'expl' and d[1] == 'there':
						expletive = d					

				head_d = dependents(head[0], sent)

				subj = 'NONE'
				subj_stem = 'NONE'
				subj_idx = ''

				for d in head_d:

					if d[7] == 'nsubj':
						subj_idx = d[0]
						subj = d[1]
						subj_stem = d[2]

				if neg == '' and subj_idx != '':
					neg = has_neg(head[0], sent)

					if len(neg) != 0:
						neg = neg[-1]
					else: 
						neg = ''

				if pred != '' and expletive == '':

					if neg != '':
						info = ['learning', function, head[2], neg[1], pred_pos, pred_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative', 'sentential']

					else:
						info = ['learning', function, head[2], '', pred_pos, pred_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'positive', 'sentential']

				if info != '':
					return info

	if age != '' and age >= 12 and age <= 72 and speaker_role in ['Target_Child', 'Child', 'Mother', 'Father'] and level == 'd':
		previous, previous_speaker_role = context(index, data)
	
		if previous != 'Nothing':

			previous_saying = [tok[1] for tok in previous]
			previous_saying = ' '.join(w for w in previous_saying)
			previous_sent_type = previous[0][-1].split()[3]

			for tok in previous:
				if tok[2] in ['be'] or tok[1] in ['am', 'was', 'is', 'are', 'were', "'m", "'s", "re"]:

					info = ''
					neg = ''

					head = previous[int(tok[6]) - 1]

					pred = ''
					pred_stem = ''
					pred_pos = ''

					if head != '' and head[3] in ['NOUN', 'PROPN', 'PRON', 'ADJ'] and head[1] not in POSS:
						pred = head[1]
						pred_stem = head[2]
						pred_pos = head[3]

					expletive = ''

					d_list = dependents(tok[0], previous)

					for d in d_list:

						if d[7] == 'expl' and d[1] == 'there':
							expletive = d					

					head_d = dependents(head[0], previous)

					subj = 'NONE'
					subj_stem = 'NONE'
					subj_idx = ''

					for d in head_d:

						if d[7] == 'nsubj':
							subj_idx = d[0]
							subj = d[1]
							subj_stem = d[2]

					if neg == '' and subj_idx != '':
						neg = has_neg(head[0], previous)

						if len(neg) != 0:
							neg = neg[-1]
						else: 
							neg = ''

					if pred != '' and expletive == '':

						if neg != '':
							info = ['learning', function, head[2], neg[1], pred_pos, pred_stem, subj, subj_stem, age, previous_speaker_role, speaker_role, previous_saying, saying, len(previous), len(sent), previous_sent_type, sent_type, corpus_name + ' ' + child_name, 'negative', 'discourse']

						else:
							info = ['learning', function, head[2], '', pred_pos, pred_stem, subj, subj_stem, age, previous_speaker_role, speaker_role, previous_saying, saying, len(previous), len(sent), previous_sent_type, sent_type, corpus_name + ' ' + child_name, 'positive', 'discourse']

					if info != '':
						return info

	return None


def perception(index, sent, corpus_name, level, data):
	
	saying = ' '.join(w[1] for w in sent)
		
	speaker_info = sent[0][-2].split()
	corpus_info = sent[0][-1].split()

	speaker_name = speaker_info[0]
	speaker_role = speaker_info[-1]

	child_name = corpus_info[0]

	sent_type = corpus_info[3]

	age = ''

	try:
		age = int(float(corpus_info[1]))

	except:
		age = ''

	if age != '' and age >= 12 and age <= 72 and speaker_role in ['Target_Child', 'Child', 'Mother', 'Father'] and level == 's':

		for tok in sent:

			if (tok[2] == 'have' or tok[1] in ['have', 'has', 'had']) and tok[3] == 'VERB':

				info = ''

				aux = 'NONE'
				aux_stem = 'NONE'
				aux_idx = ''

				subj = 'NONE'
				subj_stem = 'NONE'
				subj_idx = ''

				obj = 'NONE'
				obj_stem = 'NONE'
				obj_idx = ''
				obj_pos = ''

				neg, aux, aux_stem, aux_idx = neg_verb(tok, sent)

				d_list = dependents(tok[0], sent)

				for d in d_list:
							
					if d[3] == 'AUX' or d[7] == 'aux':
						aux = d[1]
						aux_stem = d[2]
						aux_idx = d[0]
					
					if d[7] == 'nsubj':
						subj = d[1]
						subj_stem = d[2]
						subj_idx = d[0]

					if d[7] == 'obj':
						obj = d[1]
						obj_stem = d[2]
						obj_idx = d[0]
						obj_pos = d[3]

				head = ''
				
				try:
					head = sent[int(tok[6]) - 1]
				except:
					head = tok

				### I don't have ###

				if obj == 'NONE':
					function = 'possession'

					if neg != '':
						if int(neg[0]) < int(tok[0]):						
							info = ['perception', function, 'have', neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative', 'sentential']
				
				### I don't have it ###

				if obj != 'NONE': 
					function = 'possession'

					if neg != '':
						if int(neg[0]) < int(tok[0]):						
							info = ['perception', function, 'have', neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative', 'sentential']						
					else:
						info = ['perception', function, 'have', '', aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'positive', 'sentential']
							
				if info != '':
					return info

			### mine ###
			
			if tok[1] in POSS and tok[7] == 'root':

				info = ''

				function = 'possession'

				neg = has_neg(tok[0], sent)

				cop = ''

				d_list = dependents(tok[0], sent)

				for d in d_list:
							
					if d[7] == 'cop':
						cop = d

				pre = ''

				try:
					pre = sent[int(tok[0]) - 2][1]
					if pre != 'das':
						pre = ''

				except:
					pre = ''

			#	if cop == '' and pre == '':
				if len(neg) != 0:
					info = ['perception', function, tok[1], neg[-1][1], '', '', '', '', speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative', 'sentential']
				else:
					info = ['perception', function, tok[1], '', '', '', '', '', speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'positive', 'sentential']

				if info != '':
					return info

			### there's soup ###

			if tok[2] == 'be' or tok[1] in ['am', 'was', 'is', 'are', 'were', "'m", "'s", "re"]:

				d_list = dependents(tok[0], sent)

				expletive = 'NONE'
				subj = 'NONE'

				for d in d_list:
				
					if d[7] == 'expl' and d[1] == 'there':							
						expletive = d 
				
					if d[7] == 'nsubj':
						subj = d

				if expletive != 'NONE' and subj != 'NONE' and subj[3] in ['NOUN', 'PROPN', 'PRON'] and subj[1] not in POSS:

					info = ''

					function = 'existence'

					neg = has_neg(subj[0], sent) ### there's no soup ###

					if len(neg) != 0:
						info = ['perception', function, tok[1], neg[-1][1], 'there', '', subj[1], subj[2], speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative', 'sentential']

					else:
						info = ['perception', function, tok[1], '', 'there', '', subj[1], subj[2], speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'positive', 'sentential']

					if info != '':
						return info

	if age != '' and age >= 12 and age <= 72 and speaker_role in ['Target_Child', 'Child', 'Mother', 'Father'] and level == 'd':
		previous, previous_speaker_role = context(index, data)
	
		if previous != 'Nothing':

			previous_saying = [tok[1] for tok in previous]
			previous_saying = ' '.join(w for w in previous_saying)
			previous_sent_type = previous[0][-1].split()[3]

			for tok in previous:
				if (tok[2] == 'have' or tok[1] in ['have', 'has', 'had']) and tok[3] == 'VERB':

					info = ''

					aux = 'NONE'
					aux_stem = 'NONE'
					aux_idx = ''

					subj = 'NONE'
					subj_stem = 'NONE'
					subj_idx = ''

					obj = 'NONE'
					obj_stem = 'NONE'
					obj_idx = ''
					obj_pos = ''

					neg, aux, aux_stem, aux_idx = neg_verb(tok, previous)

					d_list = dependents(tok[0], previous)

					for d in d_list:
							
						if d[3] == 'AUX' or d[7] == 'aux':
							aux = d[1]
							aux_stem = d[2]
							aux_idx = d[0]
					
						if d[7] == 'nsubj':
							subj = d[1]
							subj_stem = d[2]
							subj_idx = d[0]

						if d[7] == 'obj':
							obj = d[1]
							obj_stem = d[2]
							obj_idx = d[0]
							obj_pos = d[3]

					head = ''
				
					try:
						head = previous[int(tok[6]) - 1]
					except:
						head = tok

					### I don't have ###

					if obj == 'NONE':
						function = 'possession'

						if neg != '':
							if int(neg[0]) < int(tok[0]):						
								info = ['perception', function, 'have', neg[1], aux, aux_stem, subj, subj_stem, age, previous_speaker_role, speaker_role, previous_saying, saying, len(previous), len(sent), previous_sent_type, sent_type, corpus_name + ' ' + child_name, 'negative', 'discourse']
				
					### I don't have it ###

					if obj != 'NONE': 
						function = 'possession'

						if neg != '':
							if int(neg[0]) < int(tok[0]):						
								info = ['perception', function, 'have', neg[1], aux, aux_stem, subj, subj_stem, age, previous_speaker_role, speaker_role, previous_saying, saying, len(previous), len(sent), previous_sent_type, sent_type, corpus_name + ' ' + child_name, 'negative', 'discourse']
						else:
							info = ['perception', function, 'have', '', aux, aux_stem, subj, subj_stem, age, previous_speaker_role, speaker_role, previous_saying, saying, len(previous), len(sent), previous_sent_type, sent_type, corpus_name + ' ' + child_name, 'positive', 'discourse']
							
					if info != '':
						return info

				### mine ###
			
				if tok[1] in POSS and tok[7] == 'root':

					info = ''

					function = 'possession'

					neg = has_neg(tok[0], previous)

					cop = ''

					d_list = dependents(tok[0], previous)

					for d in d_list:
							
						if d[7] == 'cop':
							cop = d

					pre = ''

					try:
						pre = sent[int(tok[0]) - 2][1]
						if pre != 'das':
							pre = ''

					except:
						pre = ''

				#	if cop == '' and  pre == '':

					if len(neg) != 0:
						info = ['perception', function, tok[2], neg[-1][1], '', '', '', '', age, previous_speaker_role, speaker_role, previous_saying, saying, len(previous), len(sent), previous_sent_type, sent_type, corpus_name + ' ' + child_name, 'negative', 'discourse']
					else:
						info = ['perception', function, tok[2], '', '', '', '', '', '', age, previous_speaker_role, speaker_role, previous_saying, saying, len(previous), len(sent), previous_sent_type, sent_type, corpus_name + ' ' + child_name, 'positive', 'discourse']

					if info != '':
						return info

				### there's soup ###

				if tok[2] == 'be' or tok[1] in ['am', 'was', 'is', 'are', 'were', "'m", "'s", "re"]:

					d_list = dependents(tok[0], previous)

					expletive = 'NONE'
					subj = 'NONE'

					for d in d_list:
				
						if d[7] == 'expl' and d[1] == 'there':							
							expletive = d 
				
						if d[7] == 'nsubj':
							subj = d

					if expletive != 'NONE' and subj != 'NONE' and subj[3] in ['NOUN', 'PROPN', 'PRON'] and subj[1] not in POSS:

						info = ''

						function = 'existence'

						neg = has_neg(subj[0], previous) ### there's no soup ###

						if len(neg) != 0:
							info = ['perception', function, tok[1], neg[-1][1], 'there', '', subj[1], subj[2], age, previous_speaker_role, speaker_role, previous_saying, saying, len(previous), len(sent), previous_sent_type, sent_type, corpus_name + ' ' + child_name, 'negative', 'discourse']

						else:
							info = ['perception', function, tok[1], '', 'there', '', subj[1], subj[2], age, previous_speaker_role, speaker_role, previous_saying, saying, len(previous), len(sent), previous_sent_type, sent_type, corpus_name + ' ' + child_name, 'positive', 'discourse']

						if info != '':
							return info

	return None

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'path to .conllu file')
	parser.add_argument('--output', type = str, help = 'output file')
	parser.add_argument('--domain', type = str, help = 'concept domain/function')
	parser.add_argument('--desp', action = 'store_true', help = 'file for descriptive statistics')
	parser.add_argument('--individual', action = 'store_true', help = 'whether investigating individual variation')
	parser.add_argument('--level', help = 's (sentential) or d (discourse)')

	args = parser.parse_args()

	path = args.input

	all_domain = {'emotion': emotion, 'epistemic': epistemic, 'motor': motor, 'learning': learning,  'perception': perception}


	if args.desp:
	
		child_descriptive, parent_descriptive = descriptive(args.input)

		with io.open('child_descriptive.txt', 'w', encoding = 'utf-8') as f:
			f.write('Age' + '\t' + 'N_speaker' + '\t' + 'N_utterance' + '\n')
			for k, v in child_descriptive.items():
				f.write(str(k) + '\t' + '\t'.join(str(c) for c in v) + '\n')

		with io.open('parent_descriptive.txt', 'w', encoding = 'utf-8') as f:
			f.write('Age' + '\t' + 'N_speaker' + '\t' + 'N_utterance' + '\n')
			for k, v in parent_descriptive.items():
				f.write(str(k) + '\t' + '\t'.join(str(c) for c in v) + '\n')

		print('done describing age with data ')

		child_ul_descriptive, parent_ul_descriptive = uttrance_len(args.input)

		with io.open('child_ul_descriptive.txt', 'w', encoding = 'utf-8') as f:
			f.write('Sent_len' + '\t' + 'N_speaker' + '\t' + 'N_utterance' + '\n')
			for k, v in child_ul_descriptive.items():
				f.write(str(k) + '\t' + '\t'.join(str(c) for c in v) + '\n')

		with io.open('parent_ul_descriptive.txt', 'w', encoding = 'utf-8') as f:
			f.write('Sent_len' + '\t' + 'N_speaker' + '\t' + 'N_utterance' + '\n')
			for k, v in parent_ul_descriptive.items():
				f.write(str(k) + '\t' + '\t'.join(str(c) for c in v) + '\n')

		print('done describing uttrance length with data ')

	data = []

	individual_child_descriptive = [['Age','N_speaker', 'N_utterance', 'Child']]
	individual_parent_descriptive = [['Age','N_speaker', 'N_utterance', 'Child']]

	with io.open(args.output, 'w', encoding = 'utf-8') as f:
		
		for file in os.listdir(args.input):
			if file.endswith('.conllu'):

				corpus = file.split('.')[0]
			
				if args.individual:

					filename = file.split('.')[0]
					if filename in individuals:

				#		for tok in all_domain[args.domain](args.input + file):
				#			if tok[-2].split()[1] in individuals[filename]:
				#				f.write('\t'.join(str(w) for w in tok) + '\n')

						for child in individuals[filename]:
							child_descriptive, parent_descriptive = individual_descriptive(args.input + file, child)
						
							for k, v in child_descriptive.items():
								v.insert(0, k)
								v.append(filename + ' ' + child)
								individual_child_descriptive.append(v)	

							for k, v in parent_descriptive.items():
								v.insert(0, k)
								v.append(filename + ' ' + child)
								individual_parent_descriptive.append(v)		

				else:
					all_data = get_data(args.input + file)

					header = []
					
					if args.level == 's':
						header = ['Domain', 'Function', 'Head', 'Negator', 'Aux', 'Aux_stem', 'Subj', 'Subj_stem', 'Role', 'Utterance', 'Age', 'Sent_len', 'Sent_type', 'Child', 'Polarity', 'Level']

					if args.level == 'd':
						header = ['Domain', 'Function', 'Head', 'Negator', 'Aux', 'Aux_stem', 'Subj', 'Subj_stem', 'Age', 'Previous_Role', 'Role', 'Previous_Utterance', 'Utterance', 'Previous_Sent_len', 'Sent_len', 'Previous_Sent_type', 'Sent_type', 'Child', 'Polarity', 'Level']
		
					f.write('\t'.join(w for w in header) + '\n')

					for i in range(len(all_data)):

						sentence = all_data[i]

						sent_tok = all_domain[args.domain](i, sentence, corpus, args.level, all_data)
					#	discourse_tok = all_domain[args.domain](i, sentence, corpus, 'd', all_data)

						if sent_tok is not None:

							f.write('\t'.join(str(w) for w in sent_tok) + '\n')
			

		if len(individual_child_descriptive) > 1:
			with io.open('individual_child_descriptive.txt', 'w', encoding = 'utf-8') as f:
				for tok in individual_child_descriptive:
					f.write('\t'.join(str(w) for w in tok) + '\n')

			with io.open('individual_parent_descriptive.txt', 'w', encoding = 'utf-8') as f:
				for tok in individual_parent_descriptive:
					f.write('\t'.join(str(w) for w in tok) + '\n')


	print('done collecting data')




