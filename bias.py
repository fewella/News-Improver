import nltk
from nltk.corpus import wordnet

def createSentimentDictonary():#creates sentiment dictonary from vader lexicon
	
	sentimentDictionary = []
	f = open("vader_lexicon.txt","r")
	
	for line in f:#iterates through lexicon
		items = line.split("\t")
		sentimentDictionary[items[0]] = items[1]#creates entry relating word with mean sentiment value
	
	return sentimentDictionary#returns dictionary

def insertBias(news, initial, target):

	same = 1;#whether the sentiment is the same or not

	if target == 0:#if target is zero, then sentiment values should be zero
		factor = 0
	
	elif initial == 0:#if initial is zero, factor is the target
		factor = target/2
	
	elif target * initial < 0:
		factor = -1 * abs((target - initial)/initial)#finds the factor of the initial bias and target bias
		same = 0 #reverse the sentiment
	
	else:
		factor = abs((target - initial)/initial)#finds the factor of the initial bias and target bias
	
	sentimentValue = 0
	targetSentValue = 0
	sentDict = createSentimentDictonary()#creates dictonary
	separatedText = word_tokenize(news)#parses words
	partsOfSpeech = nltk.pos_tag(separatedText)#tags words
	verbs = []
	adjectives = []

	for i in range(len(partsOfSpeech)):#loops through tagged words
		
		if partsOfSpeech[i][1][0:2] == 'VB':#if it is a verb
			verbs.append((partsOfSpeech[i],i))
		
		if partsOfSpeech[i][1][0:2] == 'JJ':#if it is an adjective
			adjectives.append((partsOfSpeech[i],i))
	
	for verb in verbs:#loops through verbs
		synonyms = []
		antonyms = []
		synonymsSet = wordnet.synsets(verb[0][0])#creates synonym set
		
		for sset in synonymsSet:#loops through set
			for l in sset.lemmas():
				
				synonyms.append((l.name(), sentDict[l.name()]))#appends synonym to list
				
				for ant in l.antonyms():#this part might be fky
						antonyms.append((ant.name(), sentDict[l.name()]))

		if verb[0][0] in sentDict:#if the word is in the dictonary
			sentimentValue = sentDict[verb[0][0]]
			targetSentValue = sentimentValue * factor;
		
		replacement = verb[0]
		if same == 1:
			for synonym in synonyms:#do the things with the sentiment values
				if nltk.pos_tag(synonym[0])[0] == verb[0][1]:
					if initial < target:
						if synonym[1] > sentimentValue:
							if synonym[1] < targetSentValue:
								if replacement[1] < synonym[1]:
									replacement = synonym
					else:
						if synonym[1] < sentimentValue:
							if synonym[1] > targetSentValue:
								if replacement[1] > synonym[1]:
									replacement = synonym
		else:
			for antonym in antonyms:#do the things with the sentiment values
				if nltk.pos_tag(antonym[0])[0] == verb[0][1]:
					if initial < target:
						if antonym[1] > sentimentValue:
							if antonym[1] < targetSentValue:
								if replacement[1] < antonym[1]:
									replacement = antonym
					else:
						if antonym[1] < sentimentValue:
							if antonym[1] > targetSentValue:
								if replacement[1] > antonym[1]:
									replacement = antonym

	for adj in adjectives:#loops through adjs
		synonyms = []
		antonyms = []
		synonymsSet = wordnet.synsets(adj[0][0])#creates synonym set
		
		for sset in synonymsSet:#loops through set
			for l in sset.lemmas():
				
				synonyms.append((l.name(), sentDict[l.name()]))#appends synonym to list
				
				for ant in l.antonyms():#this part might be fky
						antonyms.append((ant.name(), sentDict[l.name()]))

		if adj[0][0] in sentDict:#if the word is in the dictonary
			sentimentValue = sentDict[adj[0][0]]
			targetSentValue = sentimentValue * factor;
		
		replacement = adj[0]
		if same == 1:
			for synonym in synonyms:#do the things with the sentiment values
				if nltk.pos_tag(synonym[0])[0] == adj[0][1]:
					if initial < target:
						if synonym[1] > sentimentValue:
							if synonym[1] < targetSentValue:
								if replacement[1] < synonym[1]:
									replacement = synonym
					else:
						if synonym[1] < sentimentValue:
							if synonym[1] > targetSentValue:
								if replacement[1] > synonym[1]:
									replacement = synonym
		else:
			for antonym in antonyms:#do the things with the sentiment values
				if nltk.pos_tag(antonym[0])[0] == adj[1]:
					if initial < target:
						if antonym[1] > sentimentValue:
							if antonym[1] < targetSentValue:
								if replacement[1] < antonym[1]:
									replacement = antonym
					else:
						if antonym[1] < sentimentValue:
							if antonym[1] > targetSentValue:
								if replacement[1] > antonym[1]:
									replacement = antonym

	for verb in verbs:
		separatedText[verb[1]] = verb[0][0]

	for adj in adjectives:
		separatedText[adj[1]] = adj[0][0]

	oldText = word_tokenize(news)
	index = 0
	foundSpace = 1
	betterNews = news
	for i in range(len(betterNews)):
		if foundSpace == 1:
			if betterNews[i:i+1] != '\"':
				betterNews = betterNews[:i] + separatedText[index] + betterNews[i + len(oldText[index])]
				foundSpace = 0

		elif betterNews[i:i+1] == ' ':
			foundSpace = 1
			index += 1
	return betterNews