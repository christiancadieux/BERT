import sys
import torch
import json
import os
from sentence_transformers import SentenceTransformer, util

from transformers import BertForQuestionAnswering
from transformers import BertTokenizer
from transformers import pipeline
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# break large document in paragraph since BERT is limited to few tokens.
# rank paragraphs based on how related they seem to be to the question

DATA="data.txt"
ans="data-qa.json"
MIN_ANSWER_SCORE=0.2
MIN_PARAGRAPH_SIMILARITY=0.4

os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

if len(sys.argv) > 1:
    DATA=sys.argv[1] + ".txt"
    ans=sys.argv[1] + "-qa.json"

f = open(ans)
QAList = json.load(f)

#Model
model = BertForQuestionAnswering.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

# Similar
similar_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


#Tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-large-uncased-whole-word-masking-finetuned-squad')

stop_words = set(stopwords.words('english'))

def correct_answer(answer):
    rc = ""
    for word in answer.split():
        if word[0:2] == '##':
            rc += word[2:]
        else:
            rc += ' ' + word
    return rc

def remove_stop_words(line):
    word_tokens = word_tokenize(line)
    filtered_line = [w for w in word_tokens if not w.lower() in stop_words]
    #print(filtered_line)
    return filtered_line


# find most related paragraph
def find_similar_paragraph(question, paragraphs):
   
    similar_q = similar_model.encode(question, convert_to_tensor=True)
    max = -100
    max_idx = -1
    par_list = []

    for idx, par0 in enumerate(paragraphs):
        par1 = par0.strip().lower()
        if par1 == "":
           continue
        similar_par = similar_model.encode(par1, convert_to_tensor=True)
        sim = util.pytorch_cos_sim(similar_q, similar_par)
        par_list.append({"idx": idx, "sim": sim[0]})

    par_list.sort(reverse=True, key=lambda d: d['sim'])
    return par_list
    

def find_answer(question, doc):
    paragraphs = doc.split('\n')

    #filtered_question = remove_stop_words(question)
    similar_par_list = find_similar_paragraph(question, paragraphs)
    for sim in similar_par_list:
       if sim["sim"] < MIN_PARAGRAPH_SIMILARITY:
          continue
       par0 = paragraphs[sim["idx"]]
       par1 = par0.strip().lower()

       scored_answers = process_paragraph(question, par1)
       print ("SIM %d=%s, PAR_SCORES=%s " % (sim["idx"], sim["sim"],  scored_answers))

       if scored_answers[0]['score'] > MIN_ANSWER_SCORE:
          return scored_answers

    print ("NO GOOD PARAGRAPH FOUND:", similar_par_list)
    return []

def process_paragraph (question, paragraph):
    print ("Q=", question, "PAR=", paragraph[0:100])
    encoding = tokenizer.encode_plus(text=question,text_pair=paragraph)

    inputs = encoding['input_ids']  #Token embeddings
    sentence_embedding = encoding['token_type_ids']  #Segment embeddings
    tokens = tokenizer.convert_ids_to_tokens(inputs) #input tokens

    nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)
    scored_answers = nlp(question=question, context=paragraph, top_k=2)

    start_scores, end_scores = model(input_ids=torch.tensor([inputs]), token_type_ids=torch.tensor([sentence_embedding]), return_dict=False)
    start_index = torch.argmax(start_scores)
    end_index = torch.argmax(end_scores)

    #answer = ' '.join(tokens[start_index:end_index+1])

    #corrected_answer = correct_answer(answer)
    return scored_answers


print ("Reading ", DATA)

with open(DATA, 'r') as file:
        document = file.read().rstrip()


count_test = 0
count_pass = 0
for qa in QAList:
  
     count_test += 1
     scored_answers = find_answer(qa["q"], document)
     if len(scored_answers) == 0:
        print ("Q=%s \n NO ANSWER" % (qa["q"],))
        continue
        
     model_ans = scored_answers[0]["answer"]

     result="FAIL"
     #print (">>>>a=%s, model=%s, %d - %d" %( qa["a"], model_ans,  qa["a"].find(model_ans) , model_ans.find(qa["a"]) ))
     if qa["a"].find(model_ans) >= 0 or model_ans.find(qa["a"]) >= 0:
        result="PASS"
        count_pass += 1
     
     print ("Q=%s\n  Answer=%s\n  Model =%s\n  %s " % ( qa["q"], qa["a"] , model_ans, result))
     print ("      SCORE      ANSWER")
     for ans in scored_answers:
       print ("      %f   %s " % (ans['score'], ans['answer']))
     print ()


print  ("Tests: %d, PASSED: %d " % (count_test, count_pass))



