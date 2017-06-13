#!/bin/bash

#update user with your GitHub username
user=ENTER_USERNAME

repos=(
"osc-core" 
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
    git clone git@github.com:$user/"${repo}".git
    cd "${repo}"/
    git remote add upstream git@github.com:opensecuritycontroller/"${repo}".git
    git remote set-url --push upstream no_push
    cd ../"${repo}"/.git/hooks 
    ln -s ../../hooks/pre-push .
    cd ../../../
done
