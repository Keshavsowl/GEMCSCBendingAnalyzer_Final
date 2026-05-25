#!/bin/bash
g++ -g -o 3DOF_Fitter.o 3DOF_Fitter.cpp $(root-config --cflags --glibs --ldflags) -lMinuit
./3DOF_Fitter.o
