all:
	make clean; make program; make run

# dla C++ wszedzie zmieniamy .c na .cpp
MAKEFLAGS = --no-print-directory

CC= g++ # dla C++:   CC=g++
UPCXX=upcxx/bin/upcxx-meta
CFLAGS= -O2 -std=c++14 
INCLUDE=
LIB= #-lpthread -lm -lgsl -lgslcblas # dla lapacka:	LIB= -lm -llapack -lblas
SOURCES= 
OBJECTS= $(SOURCES:.cpp=.o)
ARGS=

TARGET = program

$(TARGET): main.cpp $(OBJECTS)
	$(CC) -O2 -std=c++14 $(shell $(UPCXX) PPFLAGS) $(shell $(UPCXX) LDFLAGS) $(shell $(UPCXX) LIBFLAGS) -o $@ $^ $(LIB)

#.c.o:
#	$(CC) $(CFLAGS) $(INCLUDE) -c $< -o $@

#run on one machine with 4 cores
run:
	mpiexec -n 3 ./program $(ARGS)

.PHONY: clean

clean:
	rm -f  $(TARGET) *.o result*

.PHONY: echo

echo:
	echo $(shell $(UPCXX) PPFLAGS)
