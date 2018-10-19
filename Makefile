TARGET = pi
SRC = pi.cpp
CXX = g++
CXXFLAGS = -Wall -pthread -std=c++11 -O2

.PHONY = all clean

all:build
build:
	${CXX} ${CXXFLAGS} -s ${SRC} -o ${TARGET}
clean:
	@${RM} -f ${TARGET}
