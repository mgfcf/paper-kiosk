from Dictionary import default_language
from settings import language

'''Takes a collection of phrases and outputs the necessary text
according to the language and inserts parameters.'''


def get_text(dictionary, *params):
    text = dictionary[default_language]
    if language in dictionary.keys():
        text = dictionary[language]

    return __insert_params__(text, params)


def __insert_params__(text, params):
    index = 0
    while '*%d' % index in text and index < len(params):
        splitted = text.split('*%d' % index)
        text = splitted[0] + str(params[index]) + splitted[1]
        index += 1
    while '*' in text:
        splitted = text.split('*%d' % index)
        if len(splitted) > 1:
            text = splitted[0] + splitted[1].lstrip(' ')
        else:
            text = splitted[0].rsplit(' ')
        index += 1
    return text
