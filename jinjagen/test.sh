#!/bin/sh

rm -rf out
mkdir out

# test output to stdout (yaml)
mkdir out/1
./jinjagen.py -d test.yaml test1.txt.j2 > out/1/test1.txt

# test output to stdout (json)
mkdir out/2
./jinjagen.py -d test.json test1.txt.j2 > out/2/test1.txt

# test output to stdout (stdin)
mkdir out/3
./jinjagen.py -d - test1.txt.j2 < test.yaml > out/3/test1.txt

# test output
mkdir out/4
./jinjagen.py -d test.yaml -o out/4/test1.txt test1.txt.j2

# test inplace (.j2 ext)
mkdir out/5
./jinjagen.py -d test.yaml -i test1.txt.j2 && mv test1.txt out/5

# test inclace (! .2 ext)
mkdir out/6
./jinjagen.py -d test.yaml -i test2.txt && mv test2.txt.new out/6

# test inplace (multiple in)
mkdir out/7
./jinjagen.py -d test.yaml -i test3.txt test4.txt && mv test3.txt.new test4.txt.new out/7

#test inplace in subdir (j2 ext)
mkdir out/8
./jinjagen.py -d test.yaml -i sub/test1.txt.j2 && mv sub/test1.txt out/8

# test inclace (! .2 ext)
mkdir out/9
./jinjagen.py -d test.yaml -i sub/test2.txt && mv sub/test2.txt.new out/9

find out -type f | sort | xargs md5sum out.ref

