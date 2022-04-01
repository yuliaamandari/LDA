import TextMining as tm
import pandas as pd
import time
import openewfile as of


fSlang = of.openfile(path = './slangword')
bahasa = 'id'
stops, lemmatizer = tm.LoadStopWords(bahasa, sentiment = False)
sw=open(fSlang,encoding='utf-8', errors ='ignore', mode='r');SlangS=sw.readlines();sw.close()
SlangS = {slang.strip().split(':')[0]:slang.strip().split(':')[1] for slang in SlangS}


def cleanningtext (data, both = True, onlyclean = False, dropduplicate = False):
  
    start_time = time.time()
    cleantweet = []
    
    
    for i in range(0, len(data)):
        if both:
            tweet = tm.cleanText(str(data['content'][i]),fix=SlangS, pattern2 = True, lang = bahasa, lemma=None, stops = stops, symbols_remove = True, numbers_remove = True, hashtag_remove= True, min_charLen = 2)
            tweet = tm.handlingnegation(tweet)
            print(i,tweet)
            cleantweet.append(tweet)
        elif onlyclean:
            tweet = tm.cleanText(str(data['content'][i]),fix=SlangS, pattern2 = True, lang = bahasa, lemma=None, stops = stops, symbols_remove = True, numbers_remove = True, min_charLen = 3)
            #tweet = tm.handingnegation(tweet)
            print(tweet)
            cleantweet.append(tweet)
        else:
            tweet = tm.handlingnegation(str(data['content'][i]))
            print(tweet)
            cleantweet.append(tweet)
    
    print("%s seconds" %(time.time()-start_time))

    if dropduplicate:
        Dataclean = pd.DataFrame(cleantweet)
        Dataclean1 = Dataclean.drop_duplicates(keep='first')
        Dataclean1.columns = ['content']
        indexdata  =  Dataclean1.index.values    
        targetbaru = []
        for i in range(0,len(indexdata)):
            trgt = data.Label[indexdata[i]]
            targetbaru.append(trgt)
    
        target = pd.DataFrame(targetbaru)
        target.columns = ['Label']
    
        Dataclean2 = Dataclean1.reset_index(drop='True')
        data1 = pd.concat([Dataclean2,target],axis=1)
    else:
        Dataclean1 = pd.DataFrame(cleantweet)
        Dataclean1.columns = ['cleaned_content']
        data1 = pd.concat([data, Dataclean1],axis=1)
        
    return (data1)