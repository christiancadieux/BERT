import sys
import torch
import json

from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
from transformers import pipeline

DATA="data.txt"
ans="data-qa.json"

if len(sys.argv) > 1:
    DATA=sys.argv[1] + ".txt"
    ans=sys.argv[1] + "-qa.json"

f = open(ans)
QAList = json.load(f)

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

    nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
    scored_answers = nlp(question=question, context=paragraph, top_k=2)

    start_scores, end_scores = model(input_ids=torch.tensor([inputs]), token_type_ids=torch.tensor([sentence_embedding]), return_dict=False)
    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores)

    answer = ' '.join(tokens[start_index:end_index+1])

    corrected_answer = correct_answer(answer)
    return (corrected_answer.strip(), scored_answers)


print ("Reading ", DATA)

with open(DATA, 'r') as file:
        paragraph = file.read().rstrip()

print ("Paragraph:")
print (paragraph)
print ("--------------------------------------------------------\n")

count_test = 0
count_pass = 0
for qa in QAList:
     count_test += 1
     (model_ans, scored_answers) = process(qa["q"])

     result="FAIL"
     if qa["a"].find(model_ans) >= 0 or model_ans.find(qa["a"]) >= 0:
        result="PASS"
        count_pass += 1
     
     print ("Q=%s\n  Answer=%s\n  Model =%s\n  %s " % ( qa["q"], qa["a"] , model_ans, result))
     print ("      SCORE      ANSWER")
     for ans in scored_answers:
       print ("      %f   %s " % (ans['score'], ans['answer']))
     print ()


print  ("Tests: %d, PASSED: %d " % (count_test, count_pass))



