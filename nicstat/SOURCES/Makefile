# Makefile - simplified for RHEL/CentOS RPM build

FILES =	nicstat

SOURCES =	nicstat.c
BINARY =	nicstat

CC =		gcc
#-- This may be useful on RHEL versions where gcc is only version 4.1
#CC =		gcc43

COPT =		-O3

CMODEL =	-m64

CFLAGS =	$(COPT) $(CMODEL)

all : $(FILES)
	$(CC) $(CFLAGS) $(SOURCES) -o $(BINARY)

clean :
	rm -f $(FILES)
