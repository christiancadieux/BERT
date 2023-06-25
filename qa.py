import sys
import torch

from transformers import BertForQuestionAnswering
from transformers import BertTokenizer

DATA="data.txt"
if len(sys.argv) > 1:
    DATA=sys.argv[1]

#Model
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

#Tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

def correct_answer(answer):
    rc = ""
    for word in answer.split():
        if word[0:2] == '##':
            rc += word[2:]
        else:
            rc += ' ' + word
    return rc


def process (question):

    encoding = tokenizer.encode_plus(text=question,text_pair=paragraph)

    inputs = encoding['input_ids']  #Token embeddings
    sentence_embedding = encoding['token_type_ids']  #Segment embeddings
    tokens = tokenizer.convert_ids_to_tokens(inputs) #input tokens

    start_scores, end_scores = model(input_ids=torch.tensor([inputs]), token_type_ids=torch.tensor([sentence_embedding]), return_dict=False)

    start_index = torch.argmax(start_scores)

    end_index = torch.argmax(end_scores)

    answer = ' '.join(tokens[start_index:end_index+1])

    corrected_answer = correct_answer(answer)



    print(corrected_answer)


print ("Reading ", DATA )

with open(DATA, 'r') as file:
        paragraph = file.read().rstrip()

print ("Paragraph:", paragraph)

while True:
     question = input('Question? ')
     if question[0] == '#':
         print ("Bye!")
         break
     process(question)



