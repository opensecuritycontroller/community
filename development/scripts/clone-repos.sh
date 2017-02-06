#!/bin/sh

repos("osc-core"\
"vmware-nsx-plugin"\
"vmware-nsx-api"\
"security-mgr-smc-plugin"\
"security-mgr-sample-plugin"\
"security-mgr-nsm-plugin"\
"security-mgr-api"\
"sdn-controller-api"\
"security-mgr-r80-plugin"\
"sdn-controller-nsc-plugin"\
"opensecuritycontroller.org")

for repo in "${repos[@]"
do 
    :
    git clone git@github.com:opensecuritycontroller/${repo}.git
    
        
    