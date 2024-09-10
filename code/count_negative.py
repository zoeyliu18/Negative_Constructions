## Count total number of negative utterances at the sentence and discourse level

import io, os, argparse
import pandas as pd

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

		if previous_target_child_name == target_child_name and previous_target_child_id == target_child_id and previous_transcript_id == transcript_id:
			if speaker_role in ['Target_Child', 'Child'] and previous_speaker_role in ['Mother', 'Father']:
				previous = previous 
			if speaker_role in ['Mother', 'Father'] and previous_speaker_role in ['Target_Child', 'Child']:
				previous = previous 
	#		if speaker_role in ['Target_Child', 'Child'] and previous_speaker_role in ['Target_Child', 'Child']:
	#			previous = previous 

		return previous, previous_speaker_role, current
	else:
		return 'Nothing', 'Nothing', 'Nothing'


### Count N of negative constructions in each corpus

def count_neg(file):

	all_data = []
	sentence_neg_data = []
	should_not_data = []

	with open(file) as f:
		sent = conll_read_sentence(f)
		while sent is not None:
			all_data.append(sent)

			speaker_info = sent[0][-2].split()
			speaker_role = speaker_info[-1]

			corpus_info = sent[0][-1].split()

			age = ''

			try:
				age = int(float(corpus_info[1]))

			except:
				age = ''

			if age != '' and age >= 12 and age <= 72 and speaker_role in ['Target_Child', 'Child', 'Mother', 'Father']:
				n_neg = []
				for tok in sent:
					if tok[1] in ['not', 'no', "n't"]:
						n_neg.append(tok[1].lower())

				if len(n_neg) != 0 and list(set(n_neg))[0] != 'no':
					utterance = ' '.join(tok[1] for tok in sent)
				#	if "should not" in utterance or "shouldn't" in utterance:
				#		should_not_data 
					sentence_neg_data.append([file, speaker_role, age, len(n_neg), utterance])

			sent = conll_read_sentence(f)

	return all_data, sentence_neg_data

child_sentence_neg_count = []
parent_sentence_neg_count = []
#no_c = 0
child_discourse_neg_count = []
parent_discourse_neg_count = []

for file in os.listdir('../Childes_English/'):
	if file.endswith('conllu'):
		print(file)
		all_data, sentence_neg_data = count_neg('../Childes_English/' + file)
		for tok in sentence_neg_data:
			if tok[1] in ['Target_Child', ' Child']:				
				child_sentence_neg_count.append(tok)
			else:
				parent_sentence_neg_count.append(tok)
#		for tok in sentence_neg_data:
#			if tok[-1].lower() == 'no':
#				no_c += 1
		print('Done with sentence level')

		## Discourse level
		for i in range(len(all_data)):
			sentence = all_data[i]
			speaker_info = sentence[0][-2].split()
			speaker_role = speaker_info[-1]
			corpus_info = sentence[0][-1].split()
			age = ''
			try:
				age = int(float(corpus_info[1]))
			except:
				age = ''
			if age != '' and age >= 12 and age <= 72 and speaker_role in ['Target_Child', 'Child', 'Mother', 'Father']:
				previous, previous_speaker_role, current = context(i, all_data)
				if previous != 'Nothing':
				
					current_utterance = ' '.join(tok[1] for tok in sentence)

					previous_speaker_info = previous[0][-2].split()
					previous_speaker_role = previous_speaker_info[-1]
					previous_corpus_info = previous[0][-1].split()
					previous_age = ''
					try:
						previous_age = int(float(previous_corpus_info[1]))

					except:
						previous_age = ''
					previous_utterance = ' '.join(tok[1] for tok in previous)

					if previous_speaker_role in ['Mother', 'Father'] and speaker_role in ['Target_Child', 'Child']:
						child_discourse_neg_count.append([file, previous_speaker_role, previous_utterance, speaker_role, current_utterance])
					if previous_speaker_role in ['Target_Child', 'Child'] and speaker_role in ['Mother', 'Father']:
						parent_discourse_neg_count.append([file, previous_speaker_role, previous_utterance, speaker_role, current_utterance])

		print('Done with discourse level')
		print('')

print('Child sentence', len(child_sentence_neg_count))
print('Parent sentence', len(parent_sentence_neg_count))
print('Child discourse', len(child_discourse_neg_count))
print('Parent discourse', len(parent_discourse_neg_count))

with open('sentence_neg_data.txt', 'w') as f:
	header = ['Corpus', 'Speaker_role', 'Age', 'N_of_neg', 'Utterance', 'Level']
	f.write('\t'.join(z for z in header) + '\n')
	for tok in child_sentence_neg_count + parent_discourse_neg_count:
		tok.append('Sentence')
		f.write('\t'.join(str(z) for z in tok) + '\n')

with open('discourse_neg_data.txt', 'w') as f:
	header = ['Corpus', 'Previous_Speaker_role', 'Previous_Utterance', 'Speaker_role', 'Utterance']
	f.write('\t'.join(z for z in header) + '\n')
	for tok in child_discourse_neg_count + parent_discourse_neg_count:
		tok.append('Discourse')
		f.write('\t'.join(str(z) for z in tok) + '\n')
 


