from keybert import KeyBERT

kw_model = KeyBERT(model='all-mpnet-base-v2')

full_text = "Need insurance assist on my bike insurance"

keywords = kw_model.extract_keywords(full_text, keyphrase_ngram_range=(1, 3), 
                                     stop_words='english', 
                                     highlight=False,
                                     top_n=20)

keywords_list= list(dict(keywords).keys())

print(keywords_list)