# Use verilator as sim
SIM ?= verilator

# Use verilog as language
TOPLEVEL_LANG ?= verilog

# To suppress warnings
VERILATOR_ARGS += -Wno-WIDTHTRUNC -Wno-UNUSED -Wno-UNDRIVEN -Wno-CASEINCOMPLETE 

# Source code list
VERILOG_SOURCES = ../../datapath.v \
                  ../../alu.v \
                  ../../branch_compar.v \
                  ../../control_logic.v \
                  ../../dmem.v \
                  ../../imem.v \
                  ../../immgen.v \
                  ../../mux2.v \
                  ../../mux4.v \
                  ../../pc_adder.v \
                  ../../reg_file.v

# TOP LEVEL module
TOPLEVEL = datapath

# Module direct to test
MODULE = simple_datapath_test

# Include the common Makefile
include $(shell cocotb-config --makefiles)/Makefile.sim