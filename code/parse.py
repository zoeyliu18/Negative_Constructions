import io, os, string, argparse
from diaparser.parsers import Parser
import pandas as pd
import stanza

puncts = list(string.punctuation)

AUX = ['can', 'could', 'ca', 'dare', 'do', 'did', 'does', 'have', 'had', 'has', 'may', 'might', 'must', 'need', 'ought', 'shall', 'should', 'will', 'would']
COP = ['be', 'is', 'was', 'am', 'are', 'were']
SUBJ = ['you', 'she', 'he', 'they', 'it', 'we', 'i']

unintelligible = ["xxx", "xx", "yyy", "yy", "www", "ww", "zzz", "zz"]

### Loading models

en_parser = Parser.load('en_ewt-electra')
#parser = Parser.load('en_ptb-electra')

nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,lemma,depparse', tokenize_pretokenized=True)

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


def has_punct(w):

	p_l = []

	w = list(w)
	for p in puncts:
		if p in w:
			p_l.append(p)

	return p_l

### Getting POS and STEM features from Stanza ###

def get_features(sentence, speaker, child_info):

	tokens = []
	for tok in sentence:
		tokens.append(tok[1])

	utterance = ' '.join(w for w in tokens)

	parse_info = nlp(utterance)

	parse_results = []

	for sent in parse_info.sentences:

		for i in range(len(sent.words)):
			word = sent.words[i]
			w_id = sentence[i][0]
			w_text = sentence[i][1]
			w_lemma = word.lemma
			w_upos = word.upos
			w_xpos = word.xpos
			w_feats = word.feats
			w_head = sentence[i][6]
			w_deprel = sentence[i][7]
			w_speaker = speaker
			w_child_info = child_info

			parse_results.append([w_id, w_text, w_lemma, w_upos, w_xpos, w_feats, w_head, w_deprel, w_speaker, w_child_info])

	return parse_results

def parse(file, output):

	print(file)

	num_sent = 0

	file_name = file[ : -4]

	outfile = io.open(output + file_name + '.conllu', 'w', encoding = 'utf-8')

	w_punct = []

	df = pd.read_csv(output + file, encoding = 'utf-8')
	idx = df['id'].tolist()
	gloss = df['gloss'].tolist()
	stem = df['stem'].tolist()
	u_type = df['type'].tolist()
	num_morphemes = df['num_morphemes'].tolist()
	num_tokens = df['num_tokens'].tolist()
	utterance_order = df['utterance_order'].tolist()
	corpus_name = df['corpus_name'].tolist()
	pos = df['part_of_speech'].tolist()
	speaker_code = df['speaker_code'].tolist()
	speaker_name = df['speaker_name'].tolist()
	speaker_role = df['speaker_role'].tolist()
	target_child_name = df['target_child_name'].tolist()
	target_child_age = df['target_child_age'].tolist()
	target_child_sex = df['target_child_sex'].tolist()
	collection_name = df['collection_name'].tolist()
	speaker_id = df['speaker_id'].tolist()
	target_child_id = df['target_child_id'].tolist()
	transcript_id = df['transcript_id'].tolist()

	unique_target_child_id = set(target_child_id)

	for child_id in unique_target_child_id:

		child_data = []
		child_gloss = []
		child_stem = []
		child_pos = []

		speaker_feature = []
		child_feature = []

		child_transcripts_id = []
	
		for i in range(len(idx)):
			if target_child_id[i] == child_id:
				child_transcripts_id.append(int(transcript_id[i]))

		unique_child_transcripts_id = list(set(child_transcripts_id))

		unique_child_transcripts_id.sort()

		for z in range(len(unique_child_transcripts_id)):
			individual_transcript_id = unique_child_transcripts_id[z]
			transcript_data = []
			temp_transcript_data = []
			transcript_utterance_order = []

			for i in range(len(idx)):
				if target_child_id[i] == child_id and individual_transcript_id == transcript_id[i]:
				
					temp_transcript_data.append([idx[i], gloss[i], stem[i], u_type[i], num_morphemes[i], num_tokens[i], utterance_order[i], corpus_name[i], pos[i],
				speaker_code[i], speaker_name[i], speaker_role[i], target_child_name[i], target_child_age[i], target_child_sex[i], collection_name[i],
				speaker_id[i], target_child_id[i], transcript_id[i]])
					
					assert type(utterance_order[i]) is int

					transcript_utterance_order.append(utterance_order[i])

			assert len(set(transcript_utterance_order)) == len(transcript_utterance_order)

			transcript_utterance_order.sort()

			for i in range(len(transcript_utterance_order)):
				order = transcript_utterance_order[i]
				index = transcript_utterance_order.index(order)
				data = temp_transcript_data[index]
			#	transcript_data.append(data)
				child_data.append(data)
				child_gloss.append(data[1])
				child_stem.append(data[2])
				child_pos.append(data[3])

				feature = data[3] + ' ' + str(data[4]) + ' ' + str(data[5]) + ' ' + str(data[-4] + ' ' + str(data[-3]) + ' ' + str(data[-2]) + ' ' + str(data[-1]) + ' ' + str(data[6]))
				speaker_feature.append(str(data[10]) + ' ' + str(data[9]) + ' ' + str(data[11]))
				child_feature.append(str(data[12]) + ' ' + str(data[13]) + ' ' + str(data[14]) + ' ' + feature)

		new_gloss_list = []
		new_stem_list = []
		new_pos_list = []

		for i in range(len(child_gloss)):
			new_gloss = []
			new_stem = []
			new_pos = []
			if type(child_gloss[i]) is not float and type(child_stem[i]) is float:
				print('IRREGULAR')
				print(child_gloss[i])
				print(child_stem[i])

			if type(child_stem[i]) is not float and type(child_gloss[i]) is not float:

				toks = child_gloss[i].split()
				tok_stem = child_stem[i].split()
				tok_pos = child_pos[i].split()
				
				for z in range(len(toks)):
					w = toks[z]
					w_stem = '_'
					w_pos = '_'
					try:
						w_stem = tok_stem[z]
						w_pos = tok_pos[z]
					except:
						w_stem = '_'
						w_pos = '_'
		
					### e.g. don't ###
		
					if w.endswith("n't") and len(w) > 3:
						new_gloss.append(w[ : -3])
						new_gloss.append("n't")
						new_stem.append(w_stem)
						new_stem.append('not')
						new_pos.append(w_pos)
						new_pos.append('neg')
			
					### e.g. I'll ###

					elif w.endswith("'ll") and len(w) > 3:
						new_gloss.append(w[ : -3])
						new_gloss.append("'ll")
						new_stem.append(w_stem)
						new_stem.append('will')
						new_pos.append(w_pos)
						new_pos.append('aux')

					### e.g. I'm ###
		
					elif w.endswith("'m") and len(w) > 2:
						new_gloss.append(w[ : -2])
						new_gloss.append("'m")
						new_stem.append(w_stem)
						new_stem.append('be')
						new_pos.append(w_pos)
						new_pos.append('cop')

					### e.g. I'd ###

					elif w.endswith("'d") and len(w) > 2:
						new_gloss.append(w[ : -2])
						new_gloss.append("'d")
						new_stem.append(w_stem)
						new_stem.append('will')
						new_pos.append(w_pos)
						new_pos.append('aux')

					### e.g. We're ###

					elif w.endswith("'re") and len(w) > 3:
						new_gloss.append(w[ : -3])
						new_gloss.append("'re")
						new_stem.append(w_stem)
						new_stem.append('be')
						new_pos.append(w_pos)
						new_pos.append('cop')

					### e.g. We've ###

					elif w.endswith("'ve") and len(w) > 3:
						new_gloss.append(w[ : -3])
						new_gloss.append("'ve")
						new_stem.append(w_stem)
						new_stem.append('have')
						new_pos.append(w_pos)
						new_pos.append('aux')


					### e.g. She's / Mommy's book; copula vs. possessive###
		
					elif w.endswith("'s"):
						new_gloss.append(w[ : -2])
						new_gloss.append("'s")
						new_stem.append(w_stem)
						if w_pos == 'adj':
							new_stem.append("'s")
							new_pos.append('n')
							new_pos.append('poss')
						else:
							new_stem.append('be')
							if w[ : -2].lower() in SUBJ:
								new_pos.append('pro')
								new_pos.append('cop')
							else:
								new_pos.append('n')
								new_pos.append('cop')

					### combined adverbs or conjunctives ###

					elif len(has_punct(w)) != 0 and "'" not in w and "+" not in w:
						if '_' not in w:
							w_punct.append(w)

						for p in has_punct(w):
							w = w.replace(p, ' ')
				
						w = w.split()

						new_gloss.append(w[0])
						new_stem.append(w_stem)
						new_pos.append(w_pos)
					
						for c in w[1 : ]:
							new_gloss.append(c)
							new_stem.append(c)
							new_pos.append('combined')
						
					elif w in ['wanna', 'wana']:
						new_gloss.append(w[ : -2])
						new_gloss.append('na')
						new_stem.append('want')
						new_stem.append('to')
						new_pos.append('v')
						new_pos.append('inf')

					elif w in ['hafta']:
						new_gloss.append(w[ : -2])
						new_gloss.append('ta')
						new_stem.append('have')
						new_stem.append('to')
						new_pos.append('v')
						new_pos.append('inf')

					elif w in ['hasta']:
						new_gloss.append(w[ : -2])
						new_gloss.append('ta')
						new_stem.append('have')
						new_stem.append('to')
						new_pos.append('v')
						new_pos.append('inf')

					elif w in ['hadta']:
						new_gloss.append(w[ : -2])
						new_gloss.append('ta')
						new_stem.append('have')
						new_stem.append('to')
						new_pos.append('v')
						new_pos.append('inf')

					elif w in ['sposta']:
						new_gloss.append(w[ : -2])
						new_gloss.append('ta')
						new_stem.append('suppose')
						new_stem.append('to')
						new_pos.append('v')
						new_pos.append('inf')

					elif w in ['gonna']:
						new_gloss.append(w[ : -2])
						new_gloss.append('ta')
						new_stem.append('go')
						new_stem.append('to')
						new_pos.append('v')
						new_pos.append('inf')

					elif w in ['needta']:
						new_gloss.append(w[ : -2])
						new_gloss.append('ta')
						new_stem.append('need')
						new_stem.append('to')
						new_pos.append('v')
						new_pos.append('inf')

					elif w in ['lemme']:
						new_gloss.append(w[ : -2])
						new_gloss.append('me')
						new_stem.append('let')
						new_stem.append('I')
						new_pos.append('v')
						new_pos.append('pro')

					elif w in ['dunno']:
						new_gloss.append('du')
						new_gloss.append('n')
						new_gloss.append('no')
						new_stem.append('do')
						new_stem.append('not')
						new_stem.append('know')
						new_pos.append('aux')
						new_pos.append('neg')
						new_pos.append('know')

					elif w in ['shoulda', 'coulda', 'woulda', 'musta']:
						new_gloss.append(w[ : -1])
						new_gloss.append('a')
					
						if w == 'shoulda':
							new_stem.append('should')
						if w == 'coulda':
							new_stem.append('can')
						if w == 'woulda':
							new_stem.append('will')
						if w == 'musta':
							new_stem.append('must')
					
						new_stem.append('have')
						new_pos.append('aux')
						new_pos.append('aux')

					else:
						if w not in unintelligible:
							new_gloss.append(w)
							new_stem.append(w_stem)
							new_pos.append(w_pos)
						else:
							new_gloss.append('xxx')
							new_stem.append('xxx')
							new_pos.append('xxx')

			else:
				new_gloss.append('xxx')
				new_stem.append('xxx')
				new_pos.append('xxx')

			new_gloss_list.append(new_gloss)
			new_stem_list.append(new_stem)
			new_pos_list.append(new_pos)

		print(len(new_gloss_list))
		print(len(child_gloss))

		assert len(new_gloss_list) == len(child_gloss)
		assert len(new_gloss_list) == len(new_stem_list)
		assert len(new_gloss_list) == len(new_pos_list)

		####### Parsing ######

		for i in range(len(child_gloss)):
			if new_gloss_list[i] != ['xxx']:

				u = child_gloss[i]
				outfile.write('# text = ' + ' ' + u + '\n')

				try:
					temp_u = new_gloss_list[i]
					while 'xxx' in temp_u:
						temp_u.remove('xxx')
					while 'xx' in temp_u:
						temp_u.remove('xx')
					while 'yyy' in temp_u:
						temp_u.remove('yyy')
					while 'yy' in temp_u:
						temp_u.remove('yy')
					while 'www' in temp_u:
						temp_u.remove('www')
					while 'ww' in temp_u:
						temp_u.remove('ww')
					while 'zzz' in temp_u:
						temp_u.remove('zzz')
					while 'zz' in temp_u:
						temp_u.remove('zz')

					temp_parse_results = []

					parse_tree = en_parser.predict(temp_u, text = 'en').sentences[0]
					attributes = parse_tree.__dict__['values']
					attributes[2] = tuple(new_stem_list[i])
					attributes[3] = tuple(new_pos_list[i])
					attributes[-2] = tuple([speaker_feature[i]] * len(attributes[0]))
					attributes[-1] = tuple([child_feature[i]] * len(attributes[0]))

					for k in range(len(attributes[0])):
						feature = []
						for z in attributes:
							feature.append(str(z[k]))

						temp_parse_results.append(feature)

					parse_results = get_features(temp_parse_results, speaker_feature[i], child_feature[i])

					if new_gloss_list[i] == 'I want a pen an a book'.split():
						print(speaker_feature[i])
						print(child_feature[i])

					for tok in parse_results:
						outfile.write('\t'.join(str(w) for w in tok) + '\n')

					outfile.write('\n')

					num_sent += 1

				except:
					print('NO: ' + ' '.join(w for w in new_gloss_list[i]))

	print(len(df))
	print(num_sent)


if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('--output', type = str, help = 'output .conllu file')

	args = parser.parse_args()

#	path = args.input
#	os.chdir(path)

	for file in os.listdir(args.output):
		if file.endswith('.csv'):

			parse(file, args.output)
			print(file)
			print('DONE')


