CC=clang++
CXX=clang++

CXXFLAGS=-g -Wall -std=c++11

default: src/ChIP/extract_reads_from_TagAlign.cpp
	cd src/ChIP;make > out

clean:
	cd src/ChIP;make clean
