
## BERT - Small Documents

By default, BERT can only understand small documents - 512 tokens.

### sample run 

```
$ python3 qa.py  rdei
Reading  rdei.txt
Paragraph:
RDEI teams are grouping of users and kubernetes resources like namespaces, persistent volumes and Virtual IPs. 
The RDEI team owns the resources and the members of the team can access these resources.

RDEI is a Kubernetes control plane created by David Arbuckle at Concast in 2015.
--------------------------------------------------------

Q=what is rdei
  Answer=a kubernetes control plane
  Model =a kubernetes control plane
  PASS 
      SCORE      ANSWER
      0.557109   a Kubernetes control plane 
      0.137497   RDEI is a Kubernetes control plane 

Q=who created rdei
  Answer=david arbuckle
  Model =david arbuckle
  PASS 
      SCORE      ANSWER
      0.812041   David Arbuckle 
      0.068526   David Arbuckle at Concast 

Q=when was rdei created
  Answer=2015
  Model =2015
  PASS 
      SCORE      ANSWER
      0.897995   2015. 
      0.052985   2015. 

Q=where was rdei created
  Answer=concast
  Model =concast
  PASS 
      SCORE      ANSWER
      0.554667   Concast 
      0.225040   Concast in 2015. 

Q=what is a rdei team
  Answer=grouping of users and kubernetes resources like namespaces
  Model =grouping of users and kubernetes resources
  PASS 
      SCORE      ANSWER
      0.273901   grouping of users and kubernetes resources 
      0.030140   teams are grouping of users and kubernetes resources 

Q=who owns the kubernetes resources
  Answer=the rdei team
  Model =the rdei team
  PASS 
      SCORE      ANSWER
      0.592871   The RDEI team 
      0.157617   RDEI team 

Q=who can access kubernetes resources
  Answer=the members of the team
  Model =the members of the team
  PASS 
      SCORE      ANSWER
      0.551723   the members of the team 
      0.188457   members of the team 

Tests: 7, PASSED: 7 
```


## BERT - Large documents

Combined with a SentenceTransformer that can identify related sentences (question and paragraph), BERT can be used against large documents

### sample run

```
$ python qa_multi.py test

Reading  test.txt
Q= how many residents live in california PAR= california is a state in the western united states, located along the pacific coast. with nearly 39.
SIM 3=tensor([0.6820]), PAR_SCORES=[{'score': 0.5327154397964478, 'start': 97, 'end': 109, 'answer': '39.2 million'}, {'score': 0.2333034723997116, 'start': 90, 'end': 109, 'answer': 'nearly 39.2 million'}] 
Q=how many residents live in california
  Answer=million
  Model =39.2 million
  PASS 
      SCORE      ANSWER
      0.532715   39.2 million 
      0.233303   nearly 39.2 million 

Q= what is rdei PAR= rdei teams are grouping of users and kubernetes resources like namespaces, persistent volumes and vi
SIM 0=tensor([0.6271]), PAR_SCORES=[{'score': 0.5571086406707764, 'start': 210, 'end': 236, 'answer': 'a kubernetes control plane'}, {'score': 0.13749708235263824, 'start': 202, 'end': 236, 'answer': 'rdei is a kubernetes control plane'}] 
Q=what is rdei
  Answer=a kubernetes control plane
  Model =a kubernetes control plane
  PASS 
      SCORE      ANSWER
      0.557109   a kubernetes control plane 
      0.137497   rdei is a kubernetes control plane 

Q= who created rdei PAR= rdei teams are grouping of users and kubernetes resources like namespaces, persistent volumes and vi
SIM 0=tensor([0.5757]), PAR_SCORES=[{'score': 0.8120414018630981, 'start': 248, 'end': 262, 'answer': 'david arbuckle'}, {'score': 0.06852563470602036, 'start': 248, 'end': 273, 'answer': 'david arbuckle at concast'}] 
Q=who created rdei
  Answer=david arbuckle
  Model =david arbuckle
  PASS 
      SCORE      ANSWER
      0.812041   david arbuckle 
      0.068526   david arbuckle at concast 

Q= when was rdei created PAR= rdei teams are grouping of users and kubernetes resources like namespaces, persistent volumes and vi
SIM 0=tensor([0.5797]), PAR_SCORES=[{'score': 0.8979946970939636, 'start': 277, 'end': 281, 'answer': '2015.'}, {'score': 0.05298517271876335, 'start': 277, 'end': 281, 'answer': '2015.'}] 
Q=when was rdei created
  Answer=2015
  Model =2015.
  PASS 
      SCORE      ANSWER
      0.897995   2015. 
      0.052985   2015. 

Q= where was rdei created PAR= rdei teams are grouping of users and kubernetes resources like namespaces, persistent volumes and vi
SIM 0=tensor([0.5771]), PAR_SCORES=[{'score': 0.5546669363975525, 'start': 266, 'end': 273, 'answer': 'concast'}, {'score': 0.22503967583179474, 'start': 266, 'end': 281, 'answer': 'concast in 2015.'}] 
Q=where was rdei created
  Answer=concast
  Model =concast
  PASS 
      SCORE      ANSWER
      0.554667   concast 
      0.225040   concast in 2015. 

Q= what is a rdei team PAR= rdei teams are grouping of users and kubernetes resources like namespaces, persistent volumes and vi
SIM 0=tensor([0.7039]), PAR_SCORES=[{'score': 0.27390074729919434, 'start': 15, 'end': 57, 'answer': 'grouping of users and kubernetes resources'}, {'score': 0.030140258371829987, 'start': 5, 'end': 57, 'answer': 'teams are grouping of users and kubernetes resources'}] 
Q=what is a rdei team
  Answer=grouping of users and kubernetes resources like namespaces
  Model =grouping of users and kubernetes resources
  PASS 
      SCORE      ANSWER
      0.273901   grouping of users and kubernetes resources 
      0.030140   teams are grouping of users and kubernetes resources 

Q= who owns the kubernetes resources PAR= rdei teams are grouping of users and kubernetes resources like namespaces, persistent volumes and vi
SIM 0=tensor([0.5155]), PAR_SCORES=[{'score': 0.5928705930709839, 'start': 112, 'end': 125, 'answer': 'the rdei team'}, {'score': 0.15761663019657135, 'start': 116, 'end': 125, 'answer': 'rdei team'}] 
Q=who owns the kubernetes resources
  Answer=the rdei team
  Model =the rdei team
  PASS 
      SCORE      ANSWER
      0.592871   the rdei team 
      0.157617   rdei team 

Q= who can access kubernetes resources PAR= rdei teams are grouping of users and kubernetes resources like namespaces, persistent volumes and vi
SIM 0=tensor([0.5277]), PAR_SCORES=[{'score': 0.5517228841781616, 'start': 149, 'end': 172, 'answer': 'the members of the team'}, {'score': 0.1884569525718689, 'start': 153, 'end': 172, 'answer': 'members of the team'}] 
Q=who can access kubernetes resources
  Answer=the members of the team
  Model =the members of the team
  PASS 
      SCORE      ANSWER
      0.551723   the members of the team 
      0.188457   members of the team 

NO GOOD PARAGRAPH FOUND: [{'idx': 3, 'sim': tensor([0.1479])}, {'idx': 9, 'sim': tensor([0.1339])}, {'idx': 5, 'sim': tensor([0.1189])}, {'idx': 11, 'sim': tensor([0.0497])}, {'idx': 7, 'sim': tensor([0.0116])}, {'idx': 0, 'sim': tensor([-0.0082])}]
Q=where is the moon 
 NO ANSWER
Tests: 9, PASSED: 8 


```
