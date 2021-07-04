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
				if aux_tok[1].lower() in AUX: 
					aux = aux_tok[1]
					aux_stem = aux_tok[2]
					aux_idx = aux_tok[0]

			except:
				aux = 'NONE'

		elif potential[1] not in ['not', 'no', "n't"] and potential[1].endswith("n't"):
			neg = ['', "n't"]
							
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
						
						if aux_tok[1].lower() in AUX: 
							aux = aux_tok[1]
							aux_stem = aux_tok[2]
							aux_idx = aux_tok[0]

					except:
						aux = 'NONE'

			except:
				neg = ''

	return neg, aux, aux_stem, aux_idx

### get descriptive statistics of all children ###

def descriptive(file):

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

				if age != '':

					corpus_name = corpus_info[3]

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

					corpus_name = corpus_info[3]

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


### emotion: rejection ###

def emotion(file):

	data = []

	with io.open(file, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)

		while sent is not None:

			saying = ' '.join(w[1] for w in sent)
		
			speaker_info = sent[0][-2].split()
			corpus_info = sent[0][-1].split()

			speaker_name = speaker_info[0]
			speaker_role = speaker_info[-1]

			child_name = corpus_info[0]
			corpus_name = corpus_info[-5]

			age = ''

			try:
				age = int(float(corpus_info[1]))

			except:
				age = ''
				
			sent_type = ' '.join(w for w in corpus_info[4 : -3])

			for tok in sent:

				if tok[2] in ['like', 'want', 'wan'] or tok[1] in ['like', 'liked', 'want', 'wanted', 'wanna', 'wanna']: # and tok[3].startswith('v'): 

					info = ''

					### include cases such as 'I don't like book' ###

					neg, aux, aux_stem, aux_idx = neg_verb(tok, sent)

						### include cases such as 'I like no book' ??? ###

						#	except:
						#		try:
						#			d_list = dependents(tok[0], sent)
						#			obj = ''
						#			obj_neg = ''
						#			for d in d_list:
						#				if d[7] == 'obj':
						#					obj_neg = has_neg(d[0], sent)
						#					if len(obj_neg) != 0:
						#						neg = obj_neg[-1]
						#		except:
						#			neg = ''

					function = 'rejection'

					subj = 'NONE'
					subj_stem = 'NONE'
					subj_idx = ''

					d_list = dependents(tok[0], sent)

					for d in d_list:
						if d[1] in AUX or d[7] == 'aux':
							aux = d[1]
							aux_stem = d[2]
							aux_idx = d[0]

					for d in d_list:			
						if d[7] == 'nsubj':								
							subj = d[1]
							subj_stem = d[2]
							subj_idx = d[0]

					if neg != '':
						info = ['emotion', function, tok[2], neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative']

					else:
						info = ['emotion', function, tok[2], '', aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'positive']

					if info not in data and info != '' and speaker_role in ['Mother', 'Father', 'Target_Child', 'Child'] and age != '' and age >= 12 and age <= 72:

						data.append(info)

			sent = conll_read_sentence(f)

	return data

### theory of mind: epistemic ###

def epistemic(file):

	data = []

	with io.open(file, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)

		while sent is not None:
			
			saying = ' '.join(w[1] for w in sent)


			speaker_info = sent[0][-2].split()
			corpus_info = sent[0][-1].split()

			speaker_name = speaker_info[0]
			speaker_role = speaker_info[-1]

			child_name = corpus_info[0]
			corpus_name = corpus_info[-5]

			age = ''

			try:
				age = int(float(corpus_info[1]))

			except:
				age = ''

			sent_type = ' '.join(w for w in corpus_info[4 : -3])

			for tok in sent:

				if tok[2] in ['know', 'think', 'remember'] or tok[1] in ['know', 'knew', 'think', 'thought', 'remember', 'remembered']: #and tok[3].startswith('v'): 

					info = ''

					neg, aux, aux_stem, aux_idx = neg_verb(tok, sent)

					function = 'epistemic'

					subj = 'NONE'
					subj_stem = 'NONE'
					subj_idx = ''

					d_list = dependents(tok[0], sent)

					for d in d_list:
						if d[1] in AUX or d[7] == 'aux':
							aux = d[1]
							aux_stem = d[2]
							aux_idx = d[0]				

						if d[7] == 'nsubj':								
							subj = d[1]
							subj_stem = d[2]
							subj_idx = d[0] 

					if neg != '':
						info = ['theory of mind', function, tok[2], neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative']

					else:
						info = ['theory of mind', function, tok[2], '', aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'positive']

					if info not in data and info != '' and speaker_role in ['Mother', 'Father', 'Target_Child', 'Child'] and age != '' and age >= 12 and age <= 72:
						data.append(info)
			
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
				
					info = ['theory of mind', function, tok[2], "n't", 'dunno', 'do', subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative']


					if info not in data and info != '' and speaker_role in ['Mother', 'Father', 'Target_Child', 'Child'] and age != '' and age >= 12 and age <= 72:
						data.append(info)

			sent = conll_read_sentence(f)

	return data

### motor control ###

def motor(file):

	data = []

	with io.open(file, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)

		while sent is not None:

			saying = ' '.join(w[1] for w in sent)

			speaker_info = sent[0][-2].split()
			corpus_info = sent[0][-1].split()

			speaker_name = speaker_info[0]
			speaker_role = speaker_info[-1]

			child_name = corpus_info[0]
			corpus_name = corpus_info[-5]

			age = ''

			try:
				age = int(float(corpus_info[1]))

			except:
				age = ''
				
			sent_type = ' '.join(w for w in corpus_info[4 : -3])

			for tok in sent:

				if tok[3].startswith('v') and tok[1] not in ['like', 'liked', 'likes', 'want', 'wanted', 'wants', 'know', 'knew', 'knows', 'think', 'thought', 'thinks', 'remember', 'remembered', 'remembers', 'have', 'has', 'had', 'dunno']:

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

				#	if 'imperative' in sent_type and subj == 'NONE':
					if subj == 'NONE' and sent_type.startswith('imperative'):

						function = 'prohibition'
					
						if neg != '' and subj == 'NONE':
							if aux_stem == 'do':
								info = ['theory of mind', function, tok[2], neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative']

						if neg == '' and subj == 'NONE':
							info = ['theory of mind', function, tok[2], '', aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'positive']

					else:

						function = 'inability'

						if neg != '' and subj in ['I', 'i']:
							if aux_stem == 'can' or neg[1] == 'cannot':
								info = ['theory of mind', function, tok[2], neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative']

						if neg == '' and subj in ['I', 'i']:
							info = ['theory of mind', function, tok[2], '', aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'positive']

					if info not in data and info != '' and speaker_role in ['Mother', 'Father', 'Target_Child', 'Child'] and age != '' and age >= 12 and age <= 72:
						data.append(info)

			sent = conll_read_sentence(f)

	return data


### language learning: labeling ###

def learning(file):

	data = []

	with io.open(file, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)

		while sent is not None:

			saying = ' '.join(w[1] for w in sent)

			speaker_info = sent[0][-2].split()
			corpus_info = sent[0][-1].split()

			speaker_name = speaker_info[0]
			speaker_role = speaker_info[-1]

			child_name = corpus_info[0]
			corpus_name = corpus_info[-5]

			age = ''

			try:
				age = int(float(corpus_info[1]))

			except:
				age = ''
				
			sent_type = ' '.join(w for w in corpus_info[4 : -3])

			for tok in sent:

			#	if tok[2] in ['be'] and tok[7] == 'cop': # and tok[1] in ['am', 'was', 'is', 'are', 'were']:
				if tok[2] in ['be'] or tok[1] in ['am', 'was', 'is', 'are', 'were', "'m", "'s", "re"]:

					info = ''

					neg = ''
				
					try:
						potential = sent[int(tok[0])]
						if potential[1] in ['not', 'no', "n't"]:
							neg = potential

					except:
						neg = ''

					head = sent[int(tok[6]) - 1]

					pred = ''
					pred_stem = ''
					pred_pos = ''

					if head != '' and (head[3] in ['n', 'n:pt'] or head[3].startswith('adj') or head[3].startswith('pro')) and head[1] not in POSS:
						pred = head[1]
						pred_stem = head[2]
						pred_pos = head[3]

					function = 'labeling'

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
							info = ['learning', function, head[2], neg[1], pred_pos, pred_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative']

						else:
							info = ['learning', function, head[2], '', pred_pos, pred_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'positive']

					if info not in data and info != '' and speaker_role in ['Mother', 'Father', 'Target_Child', 'Child'] and age != '' and age >= 12 and age <= 72:
						data.append(info)

			sent = conll_read_sentence(f)

	return data


### Perception ###

def perception(file):

	data = []

	with io.open(file, encoding = 'utf-8') as f:
		sent = conll_read_sentence(f)

		while sent is not None:

			saying = ' '.join(w[1] for w in sent)

		
			speaker_info = sent[0][-2].split()
			corpus_info = sent[0][-1].split()

			speaker_name = speaker_info[0]
			speaker_role = speaker_info[-1]

			child_name = corpus_info[0]
			corpus_name = corpus_info[-5]

			age = ''

			try:

				age = int(float(corpus_info[1]))

			except:

				age = ''

			sent_type = ' '.join(w for w in corpus_info[4 : -3])

			### have the toy ###

			for tok in sent:

				if (tok[2] == 'have' or tok[1] in ['have', 'has', 'had']): #and tok[7] != 'aux':

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
							
						if d[1] in AUX or d[7] == 'aux':
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
						
								info = ['perception', function, tok[2], neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative']
				
					### I don't have it ###

					if obj != 'NONE': # and (obj_pos in ['n', 'n:pt'] or obj_pos.startswith('pro')):
						function = 'possession'

						if neg != '':
							if int(neg[0]) < int(tok[0]):
								if speaker_role in ['Target_Child', 'Child']:
									print(sent)
						
								info = ['perception', function, tok[2], neg[1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative']
						
						else:
							info = ['perception', function, tok[2], '', aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'positive']
							
					### I have no book ###

				#	if len(neg) == 0 and obj != 'NONE': # and (obj_pos in ['n', 'n:pt'] or obj_pos.startswith('pro')):

				#		obj_neg = has_neg(obj_idx, sent)

				#		if len(obj_neg) != 0:

				#			function = 'possession'
						
				#			info = ['perception', function, tok[2], obj_neg[-1][1], aux, aux_stem, subj, subj_stem, speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative']
								
					if info not in data and info != '' and speaker_role in ['Mother', 'Father', 'Target_Child', 'Child'] and age != '' and age >= 12 and age <= 72:
						data.append(info)

			### mine ###
			### exclude there's mine ###
			
				if tok[1] in POSS and tok[7] == 'root':


					d_list = dependents(tok[0], sent)

					expletive = 'NONE'

					for d in d_list:

						if d[7] == 'expl' and d[1] == 'there':
							expletive = d

					if expletive == 'NONE':
						try:
							if sent[int(tok[0]) - 2][1] == 'there':
								expletive = 'there'
					
						except:
							expletive = 'NONE'

					if expletive == 'NONE':

						info = ''

						function = 'possession'

						neg = has_neg(tok[0], sent)

						if len(neg) != 0:

							info = ['perception', function, tok[1], tok[2], neg[-1][1], '', '', '', speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative']

						else:
							info = ['perception', function, tok[1], tok[2], '', '', '', '', speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'positive']

						if info not in data and info != '' and speaker_role in ['Mother', 'Father', 'Target_Child', 'Child'] and age != '' and age >= 12 and age <= 72:
							data.append(info)


	#		### more milk ###

	#		for tok in sent:
			
	#			if tok[1] not in POSS and tok[7] == 'root' and (tok[3] in ['n', 'n:pt'] or tok[3].startswith('pro')):

	#				d_list = dependents(tok[0], sent)

	#				copula = 'NONE'

	#				for d in d_list:

	#					if d[7] == 'cop':
	#						copula = d

	#				function = 'existence'

	#				if copula == 'NONE':
	#					if len(has_neg(tok[0], sent)) != 0:

	#						info = ['perception', function, 'root', tok[2], '_', '_', '_', '_', speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative']

	#					else:

	#						info = ['perception', function, 'root', tok[2], '_', '_', '_', '_', speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'positive']

	#		if info not in data:
	#			data.append(info)


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

					if expletive != 'NONE' and subj != 'NONE': # and (subj[3] in ['n', 'n:pt'] or subj[3].startswith('pro')): # and subj[1] not in POSS:

						info = ''

						function = 'existence'

						neg = has_neg(subj[0], sent) ### there's no soup ###

						if len(neg) != 0:

							info = ['perception', function, tok[1], neg[-1][1], 'there', '', subj[1], subj[2], speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'negative']

						else:

							info = ['perception', function, tok[1], '', 'there', '', subj[1], subj[2], speaker_role, saying, age, len(sent), sent_type, corpus_name + ' ' + child_name, 'positive']


						if info not in data and info != '' and speaker_role in ['Mother', 'Father', 'Target_Child', 'Child'] and age != '' and age >= 12 and age <= 72:
							data.append(info)

			sent = conll_read_sentence(f)

	return data



if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--input', type = str, help = 'path to .conllu file')
	parser.add_argument('--output', type = str, help = 'output file')
	parser.add_argument('--domain', type = str, help = 'concept domain/function')
	parser.add_argument('--desp', help = 'file for descriptive statistics')
	parser.add_argument('--individual', help = 'whether investigating individual variation')
	parser.add_argument('--ind_desp', help = 'whether to generate descriptive files for individual children')

	args = parser.parse_args()

	path = args.input

	all_domain = {'emotion': emotion, 'motor': motor, 'learning': learning, 'epistemic': epistemic, 'perception': perception}


	if args.desp:
	
		child_descriptive, parent_descriptive = descriptive(args.input)

		with io.open(args.desp + 'child_descriptive.txt', 'w', encoding = 'utf-8') as f:
			f.write('Age' + '\t' + 'N_speaker' + '\t' + 'N_utterance' + '\n')
			for k, v in child_descriptive.items():
				f.write(str(k) + '\t' + '\t'.join(str(c) for c in v) + '\n')

		with io.open(args.desp + 'parent_descriptive.txt', 'w', encoding = 'utf-8') as f:
			f.write('Age' + '\t' + 'N_speaker' + '\t' + 'N_utterance' + '\n')
			for k, v in parent_descriptive.items():
				f.write(str(k) + '\t' + '\t'.join(str(c) for c in v) + '\n')

		print('done describing data')

	data = []

	individual_child_descriptive = [['Age','N_speaker', 'N_utterance', 'Child']]
	individual_parent_descriptive = [['Age','N_speaker', 'N_utterance', 'Parent']]

	all_child_names = {}

#	for file in os.listdir(args.input):
#		if file.endswith('csv'):
#			filename = file.split('.')[0]
#			all_child_names[filename] = []
#			data = pd.read_csv(args.input + file, encoding = 'utf-8')
#			target_child_names = set(data['target_child_name'].tolist())
#			for name in target_child_names:
#				if type(name) is str:
#					name = filename + ' ' + name
#					all_child_names[filename].append(name)

	with io.open(args.output, 'w', encoding = 'utf-8') as f:
		f.write('Domain' + '\t' + 'Function' + '\t' + 'Head' + '\t' + 'Negator' + '\t' + 'Aux' + '\t' 'Aux_stem' + '\t' + 'Subj' + '\t' + 'Subj_stem' + '\t' + 'Role' + '\t' + 'Utterance' + '\t' + 'Age' +  '\t' + 'Sent_len' + '\t' + 'Sent_type' + '\t' + 'Child' + '\t' + 'Polarity' + '\n')		
		
		for file in os.listdir(args.input):
			if file.endswith('conllu'):
			
				if args.individual == 'yes':

					filename = file.split('.')[0]
					if filename in individuals:

				#		for tok in all_domain[args.domain](args.input + file):
				#			if tok[-2].split()[1] in individuals[filename]:
				#				f.write('\t'.join(str(w) for w in tok) + '\n')

						if args.ind_desp:
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
					for tok in all_domain[args.domain](args.input + file):
						f.write('\t'.join(str(w) for w in tok) + '\n')

		if len(individual_child_descriptive) > 1:
			with io.open(args.ind_desp + 'individual_child_descriptive.txt', 'w', encoding = 'utf-8') as f:
				for tok in individual_child_descriptive:
					f.write('\t'.join(str(w) for w in tok) + '\n')

			with io.open(args.ind_desp + 'individual_parent_descriptive.txt', 'w', encoding = 'utf-8') as f:
				for tok in individual_parent_descriptive:
					f.write('\t'.join(str(w) for w in tok) + '\n')


	print('done collecting data')



