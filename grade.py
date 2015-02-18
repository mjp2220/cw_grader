import csv
import os
import re

folder = 'Homework #2'
grade_file = '{}/{}'.format(folder, 'grades.csv')
get_uni = re.compile('.*\((\w+)\)')

# walk grades folder to match UNI's to folders
directory = dict()
for s in os.listdir(folder):
    x = get_uni.search(s)
    if x:
        # uni --> folder_name
        directory[x.group(1)] = s

csv_file = 'spreadsheet.csv'
rows_to_skip = 2
UNI = 'uni'

comment_format = '''
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
'''.replace('\n', '<br>')

grades = dict()

with open(csv_file, 'rb') as f:
    [f.readline() for _ in range(rows_to_skip)]

    grade_reader = csv.DictReader(f)
    for row in grade_reader:
        uni = row.get(UNI)
        dir_name = directory.get(uni)

        if dir_name:
            grades[uni] = row.get('total')
            filename = '{}/{}/comments.txt'.format(folder, dir_name)
            with open(filename, 'w') as g:
                g.write(comment_format.format(**row))


with open(grade_file, 'rb') as f, open('final.csv', 'wb') as g:
    for _ in range(2):
        g.write(f.readline())

    grade_reader = csv.DictReader(f)
    grade_writer = csv.DictWriter(g, fieldnames=grade_reader.fieldnames)
    grade_writer.writeheader()

    for row in grade_reader:
        row['grade'] = grades.get(row.get('ID'), 0)
        grade_writer.writerow(row)


os.rename('final.csv', grade_file)

