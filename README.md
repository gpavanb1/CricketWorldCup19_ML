# CricketWorldCup_ML

![Made with Love in India](https://madewithlove.org.in/badge.svg)

This repository contains codes where 
different predictive techniques 
have been applied to the Cricket World Cup
2019 data

## Modules 

* Predicting pool stage outcome using 
Monte Carlo method - the prior is based 
on the performance of teams in the last 
10 matches against each other

## How to install and execute
Install the requirements using `pip install -r requirements.txt`

Once completed successfully, just run `main.py`

## Sample Output

This section outlines the sample outputs
from various modules in the repository

### Pool Stage Monte-Carlo
```
+----+--------+---------------+
|    | Team   |   Probability |
|----+--------+---------------|
|  0 | IND    |       0.9733  |
|  1 | ENG    |       0.9353  |
|  2 | NZ     |       0.84915 |
|  3 | AUS    |       0.581   |
|  4 | PAK    |       0.2947  |
|  5 | WI     |       0.13125 |
|  6 | RSA    |       0.0991  |
|  7 | SL     |       0.077   |
|  8 | BAN    |       0.0592  |
+----+--------+---------------+
```

## Whom to contact?

Please direct your queries to either [gpavanb1](http://github.com/gpavanb1)
for any questions. Credits to [ABK]() 
and [Cricbuzz](http://cricbuzz.com) for the web-scraping.