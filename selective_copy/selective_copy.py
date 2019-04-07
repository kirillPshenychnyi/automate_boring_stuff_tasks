#! /usr/bin/python3

"""selective copy of files"""

import os
import shutil
import argparse

def runCopy():
    parser = argparse.ArgumentParser()

    parser.add_argument('source', type=str, help='path to folder for analysis')
    parser.add_argument('destination', type=str, help='path to destination folder')
    parser.add_argument('filter', type=str, help='files extension to copy', nargs='+')

    args = parser.parse_args()

    if not os.path.isdir(args.source):
        print('% is not a dir' % args.source)
        exit(-1)

    if not os.path.isdir(args.destination):
        os.mkdir(args.destination)

    filter_set = set(args.filter)

    print(filter_set)
    for folderName, subfolders, files in os.walk(args.source):
        print('Analyzing folder %s' % folderName)
        for file in files:
            if os.path.splitext(file)[1] in filter_set:
               copy_path = os.path.join(folderName, file)
               print('Copying %s to %s' % (copy_path, args.destination))
               shutil.copy(copy_path, args.destination)



if __name__ == "__main__":
    runCopy()
