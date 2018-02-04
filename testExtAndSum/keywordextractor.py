import argparse

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types


def keyword_analysis(string):
    '''
    export GOOGLE_APPLICATION_CREDENTIALS="/Users/bohaohan/learn/hackthon/DataCleanAndSum-0401e1ef3883.json"
    :param string:
    :return:
    '''
    explicit()
    ''' Input argument: .txt file'''  
    with open('FoxStopList.txt','r') as stopList:
        stopWords = stopList.read().strip().split()
      
    client = language.LanguageServiceClient() #Initiates LanguageServiceClient as client.
    # with open(file, 'r', encoding="utf-8-sig") as f: #reads input file.
    #     text = f.read()
    text = string
    # Instantiates a plain text document with the contents being that of the opened file.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')
    count = 0
    keywords = [] #Creates an empty array to accept found keywords

    #Iterates through the entities found in decreasing order of salience (relevancy) until it reaches a "stopword" (common English words like "some") 
    #Returns the list "keywords" containing all the keywords found in order of salience.
    for entity in entities:
        if entity.name.lower() in stopWords: 
            break
        print('=' * 20)
        print(u'{:<16}: {}'.format('name', entity.name))
        print(u'{:<16}: {}'.format('salience', entity.salience)) #Salience = measure of the "relevance" of the word. Is between 0 and 1.
        keywords.append(entity.name)
    return keywords


def explicit():
    from google.cloud import storage

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        '/Users/bohaohan/learn/hackthon/DataCleanAndSum-0401e1ef3883.json')

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)


def keywordsToFile(inputList, outputfilename):
    '''Creates a file of keywords, sorted in a column of alphabetical order'''
    sortedList = sorted(inputList, key=str.lower)
    if not outputfilename.endswith('.txt'):
        outputfilename += '.txt'
    with open(outputfilename, 'w') as output:
        for word in sortedList:
            output.write(word)
            output.write('\n')
    print(sortedList)

if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    # parser.add_argument('text_to_be_analyzed', help='The filename to be analyzed for keywords.')
    # args = parser.parse_args()
    #
    pass
    # answer = keyword_analysis(args.text_to_be_analyzed)
    # keywordsToFile(answer, 'potato')
