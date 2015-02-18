import csv
import os
import re
import argparse

UNI = 'uni'


parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('spreadsheet', metavar='S', type=str,
                    help='CSV from GDrive with grades')
parser.add_argument('skip_lines', metavar='N', type=int,
                    help='number of redundant rows in the spreadsheet')
parser.add_argument('grades_dir', metavar='D', type=str,
                    help='directory for all grades')
parser.add_argument('comment_file', metavar='C', type=str,
                    help='file with comment format')
args = parser.parse_args()


folder = args.grades_dir
grade_file = os.path.join(folder, 'grades.csv')
get_uni = re.compile('.*\((\w+)\)')

# walk grades folder to match UNI's to folders
directory = dict()
for s in os.listdir(folder):
    x = get_uni.search(s) # pull the UNI from the dir name
    if x:
        # uni --> folder_name
        directory[x.group(1)] = s

# read the comment format into memory
with open(args.comment_file) as f:
    comment_format = f.read().replace('\n', '<br>')


grades = dict() # stores the total grade
with open(args.spreadsheet, 'rb') as f:
    # read in redundant rows
    [f.readline() for _ in range(args.skip_lines)]

    # process each row creating the comment file
    for row in csv.DictReader(f):
        uni = row.get(UNI)
        dir_name = directory.get(uni)

        if dir_name: # some UNI's may not be in the
            grades[uni] = row.get('total')
            comment_file = os.path.join(folder, dir_name, 'comments.txt')
            with open(comment_file, 'w') as g:
                g.write(comment_format.format(**row))  # lol dynamic languages
        else:
            print uni
            print dir_name


with open(grade_file, 'rb') as f, open('final.csv', 'wb') as g:
    for _ in range(2):
        g.write(f.readline())

    # create CSV reader and prep the writer
    grade_reader = csv.DictReader(f)
    grade_writer = csv.DictWriter(g, fieldnames=grade_reader.fieldnames)
    grade_writer.writeheader()

    # write in the new grades
    for row in grade_reader:
        row['grade'] = grades.get(row.get('ID'), 0)
        grade_writer.writerow(row)

# replace final grades file
os.rename('final.csv', grade_file)
