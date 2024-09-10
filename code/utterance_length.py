### Calculate average proportion of utterances with fewer than 10 tokens

import io, os, sys
import pandas as pd

path = sys.argv[1]

domains = ['emotion', 'epistemic', 'learning', 'motor']

sentence_utterances_length = []
sentence_c = 0
discourse_utterances_length = []
discourse_c = 0

for domain in domains:
	sentence_data = pd.read_csv(path + domain + '.txt', sep = '\t')
	utterances = sentence_data['Utterance'].tolist()
	for utt in utterances:
		utt = utt.split()
		utt_len = len(utt)
		if utt_len <= 10:
			sentence_c += 1
		sentence_utterances_length.append(utt_len)

	discourse_data = pd.read_csv(path + domain + '_discourse.txt', sep = '\t')
	utterances = discourse_data['Utterance'].tolist()
	for utt in utterances:
		utt = utt.split()
		utt_len = len(utt)
		if utt_len < 10:
			discourse_c += 1
		discourse_utterances_length.append(utt_len)

print(round(100 * sentence_c / len(sentence_utterances_length), 2))
print(round(100 * discourse_c / len(discourse_utterances_length), 2))
# emotion 86.07
# emotion discourse 98.03