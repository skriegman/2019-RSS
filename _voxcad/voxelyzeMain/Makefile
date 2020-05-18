LIBRARY_ROOT_PATH = $(HOME)


VOXELYZE_VERSION = voxelyze.0.9
# VOXELYZE_LIB_NAME = lib$(VOXELYZE_VERSION).a
VOXELYZE_PATH = ../Voxelyze/

LIBRARY_INCLUDES = \
		-I$(VOXELYZE_PATH)



# compiler flags
# -g --Enable debugging
# -Wall --Turn on all warnings
# -D_USE_FIXED_PROTOTYPES_
# --Force the compiler to use the correct headers
# -ansi --Don't use GNU ext; do use ansi standard.
#
# may have to run "source /opt/intel/composerxe/bin/compilervars.sh intel64" to get intel compiler?

# CXX=icpc
# CC=icpc
CXX=g++
CC=g++


#OPTFLAGS = -Wall -O3 -march=i686 -fforce-addr -fomit-frame-pointer -funroll-loops -frerun-cse-after-loop -frerun-loop-opt -falign-functions=4
#OPTFLAGS = -Wall -O2 -march=i686 -fforce-addr -fomit-frame-pointer -funroll-loops -frerun-cse-after-loop -frerun-loop-opt -falign-functions=4
#OPTFLAGS = -Wall -O2 -fforce-addr -fomit-frame-pointer -funroll-loops -frerun-cse-after-loop -frerun-loop-opt -falign-functions=4
#OPTFLAGS = -xhost -O3 -Wall
OPTFLAGS = -g -Wall


CFLAGS= $(OPTFLAGS) $(LIBRARY_INCLUDES)
CPPFLAGS= $(CFLAGS)


LINK =  \
	-L$(VOXELYZE_PATH) -l$(VOXELYZE_VERSION) \
	-lm -lstdc++



all: voxelyze



voxelyze:	main.o
		$(CC) $(CFLAGS) main.o $(LINK) -o voxelyze


main.o:		main.cpp
		$(CC) $(CFLAGS) -c main.cpp

oa_ex1:		main.o
		$(CC) $(CFLAGS) main.o $(LINK) -o oa_ex1


clean:
	rm -rf *.o voxelyze */*.o
