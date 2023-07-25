
SIM ?= verilator
EXTRA_ARGS += --coverage
EXTRA_ARGS += --trace --trace-structs

# Verilator exits when faces any warnings. Since debugging them is not 
# the purpose of this testbench, this line was added to allow compilation
# to proceed ignoring them.
EXTRA_ARGS += -Wno-fatal

TOPLEVEL_LANG ?= verilog

VERILOG_SOURCES += $(PWD)/../rtl/scr1_pipe_ialu.sv
VERILOG_INCLUDE_DIRS += $(PWD)/../rtl/ 
TOPLEVEL = scr1_pipe_ialu

MODULE = ialu_test

include $(shell cocotb-config --makefiles)/Makefile.sim
