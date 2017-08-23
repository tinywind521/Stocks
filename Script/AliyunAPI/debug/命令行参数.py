#!/usr/bin/python3

import sys
import getopt


def main(argv):
    inputFile = ''
    outputFile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["iFile=", "oFile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--iFile"):
            inputFile = arg
        elif opt in ("-o", "--oFile"):
            outputFile = arg
    print('输入的文件为：', inputFile)
    print('输出的文件为：', outputFile)

if __name__ == "__main__":
    main(sys.argv[1:])