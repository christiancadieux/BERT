
## sample run 

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
