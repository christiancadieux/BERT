
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

Q=who created rdei
  Answer=david arbuckle
  Model =david arbuckle
  PASS 

Q=when was rdei created
  Answer=2015
  Model =2015
  PASS 

Q=where was rdei created
  Answer=concast
  Model =concast
  PASS 

Q=what is a rdei team
  Answer=grouping of users and kubernetes resources like namespaces
  Model =grouping of users and kubernetes resources
  PASS 

Q=who owns the kubernetes resources
  Answer=the rdei team
  Model =the rdei team
  PASS 

Q=who can access kubernetes resources
  Answer=the members of the team
  Model =the members of the team
  PASS 

Tests: 7, PASSED: 7 

```
