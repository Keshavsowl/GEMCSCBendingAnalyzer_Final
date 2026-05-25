#!/bin/bash
g++ -g -o 6DOF_Fitter.o 6DOF_Fitter.cpp $(root-config --cflags --glibs --ldflags) -lMinuit
./6DOF_Fitter.o
