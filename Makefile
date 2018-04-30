all:
	make clean; make program; make run

# dla C++ wszedzie zmieniamy .c na .cpp
MAKEFLAGS = --no-print-directory

CC= g++ # dla C++:   CC=g++
CFLAGS= -O2 -std=c++14 
INCLUDE=
LIB= #-lpthread -lm -lgsl -lgslcblas # dla lapacka:	LIB= -lm -llapack -lblas
SOURCES= 
OBJECTS= $(SOURCES:.cpp=.o)
ARGS=
UPCXX_INSTALL=upcxx/
PPFLAGS=$(shell $(UPCXX_INSTALL)/bin/upcxx-meta PPFLAGS)
LDFLAGS=$(shell $(UPCXX_INSTALL)/bin/upcxx-meta LDFLAGS)
LIBFLAGS=$(shell $(UPCXX_INSTALL)/bin/upcxx-meta LIBFLAGS)

TARGET = program

$(TARGET): main.cpp $(OBJECTS)
	$(CC) -O2 -std=c++14 $< $(PPFLAGS) $(LDFLAGS) $(EXTRA_FLAGS) $(LIBFLAGS) -o $@
	
run:
	$(UPCXX_INSTALL)/bin/upcxx-run -n 3 $(TARGET) $(ARGS)

.PHONY: clean

clean:
	rm -f  $(TARGET) *.o result*

.PHONY: echo

install:
	rm -rf upcxx
	mkdir upcxx
	cd upcxx-2018.3.0
	./install ../upcxx

echo:
	echo $(shell $(UPCXX) PPFLAGS)
