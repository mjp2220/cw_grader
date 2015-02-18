
# CW Grader


Takes a CSV filled with grades and comments and generates a Courseworks upload-able directory.


Usage:
```
usage: grade.py [-h] S N D C

Process some integers.

positional arguments:
  S           CSV from GDrive with grades
  N           number of redundant rows in the spreadsheet
  D           directory for all grades
  C           file with comment format

optional arguments:
  -h, --help  show this help message and exit
```


### Example
```
python grade.py spreadsheet.csv 2 Homework\ \#2 ~/github/grader/comment.txt
```

Where the Comment file is in this format.
Every column *can* be used as input to the comment format (access with `{}` by name).

```
Homework #2

Student: {uni}

Grader: {grader}

SignUp: {signup}/20
{signup_comments}

Login {login}/45
{login_comments}

Admin/List Users {admin}/20
{admin_comments}

AWS: {aws}/15
{aws_comments}

Extra Credit: {extracredit}/10
{extracredit_comments}

Total:
    {total}/100
```
