#!/bin/bash

echo "save_attempts,shots_against"
for i in {1..38};
do
  saves=$(grep "^$i,Huskies.*Save" fullevents.csv | wc -l)
  shots=$(grep "^$i,Opponent.*Shot" fullevents.csv | wc -l)
  echo "$saves,$shots"
done
