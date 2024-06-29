import re


def remove_text_inside_brackets(text):
    pattern = r'\\u3010.*?\\u3011'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


def remove_text_inside_legacy_brackets(text):
    pattern = r'【.*?】'
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text


'''
Case:

print(
    remove_text_inside_brackets(
        'Achieved through increased demand across all business areas and regions, supported by the decentralized  operating model【4:0†source】'
    )
)
'''
