#!/bin/bash

echo "save_attempts,shots_against"
for i in {1..38};
do
  saves=$(grep "^$i,Opponent.*Save" fullevents.csv | wc -l)
  shots=$(grep "^$i,Huskies.*Shot" fullevents.csv | wc -l)
  echo "$saves,$shots"
done
