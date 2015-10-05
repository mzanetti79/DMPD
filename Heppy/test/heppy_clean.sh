#!/bin/bash

# | sed 's/ //g' | grep Batch | sed ':a;N;$!ba;s/\n/ /g' | sed 's/;.*//' | sed 's/t\///' | awk '{ print $1 }'

for i in `bjobs -d | grep EXIT  | awk '{ print $1 }'`
do
    text=`bjobs -l $i  | sed ':a;N;$!ba;s/\n//g'  | sed 's/ //g' | sed 's/;/\n/g' | grep cd/ | sed 's/cd\//\//g'`
    echo $i $text
done


