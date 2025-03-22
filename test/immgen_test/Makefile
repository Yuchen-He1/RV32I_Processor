



# use verilator as sim
SIM ?= verilator

# use verilog as language
TOPLEVEL_LANG ?= verilog

# source code list 
VERILOG_SOURCES = ../../immgen.v
#$(shell find ../../ -name "*.v")
#TOP LEVEL module

TOPLEVEL = immgen

# module direct to test
MODULE = immgen_test

# include the common Makefile
include $(shell cocotb-config --makefiles)/Makefile.sim