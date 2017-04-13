#!/bin/bash

repos=(
"osc-core" 
"vmware-nsx-plugin" 
"vmware-nsx-api" 
"security-mgr-smc-plugin"
"security-mgr-sample-plugin"
"security-mgr-nsm-plugin"
"security-mgr-api"
"sdn-controller-api"
"sdn-controller-nsc-plugin"
"opensecuritycontroller.org"
"community"
)

for repo in "${repos[@]}"
do 
    git clone git@github.com:opensecuritycontroller/"${repo}".git
    cd "${repo}"/.git/hooks
    ln -s ../../hooks/pre-push .
    cd ../../../
done
