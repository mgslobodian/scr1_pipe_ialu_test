
from fixedint import*
import itertools  
from enum import Enum
import random as rnd

import cocotb
from cocotb.triggers import Timer
from cocotb_coverage.coverage import CoverPoint, CoverCross, coverage_db

N_TEST = 1_000_000
SEED = 2023

SCR1_XLEN = 32

class Cmd(Enum):
	ADD = 4 	 # SCR1_IALU_CMD_ADD
	SUB = 5 	 # SCR1_IALU_CMD_SUB

MAX_IN = 2**(SCR1_XLEN-1)-1
MIN_IN = -2**(SCR1_XLEN-1)

VALUES_OF_INTEREST = (MAX_IN, MIN_IN, 0, -1, 1)
COVERAGE_LABELS = ['MAX', 'MIN', '0', '-1', '1']

@cocotb.test()
async def addition(dut):
	rnd.seed(SEED)
	operands = []
	for i in range(N_TEST):
		op1 = rnd.randint(MIN_IN, MAX_IN)
		op2 = rnd.randint(MIN_IN, MAX_IN)
		operands += (op1, op2, ),

	await run_test(dut, operands, Cmd.ADD)
	
@cocotb.test()
async def add_edge_cases(dut):
	# get all possible pairs of VALUES_OF_INTEREST
	operands = list(itertools.product(VALUES_OF_INTEREST, repeat = 2))
	await run_test(dut, operands, Cmd.ADD)

@cocotb.test()
async def subtraction(dut):
	rnd.seed(SEED)
	operands = []
	for i in range(N_TEST):
		op1 = rnd.randint(MIN_IN, MAX_IN)
		op2 = rnd.randint(MIN_IN, MAX_IN)
		operands += (op1, op2, ),
	
	await run_test(dut, operands, Cmd.SUB)

@cocotb.test()
async def sub_edge_cases(dut):
	# get all possible pairs of VALUES_OF_INTEREST
	operands = list(itertools.product(VALUES_OF_INTEREST, repeat = 2))
	await run_test(dut, operands, Cmd.SUB)
	coverage_db.export_to_xml(filename="coverage.xml")


@CoverPoint("top.op1", vname="op1", 
			bins = list(VALUES_OF_INTEREST), bins_labels = COVERAGE_LABELS)
@CoverPoint("top.op2", vname="op2", 
			bins = list(VALUES_OF_INTEREST), bins_labels = COVERAGE_LABELS)
@CoverPoint("top.cmd", vname = "cmd", bins = [Cmd.ADD.name, Cmd.SUB.name])
@CoverCross("top.edge_cases", items = ["top.op1", "top.op2", "top.cmd"]) 


def sample(op1, op2, cmd):
    pass

async def run_test(dut, operands, cmd):
	
	dut.exu2ialu_cmd_i.value = cmd.value

	for ops in operands:

		op1, op2 = Int32(ops[0]), Int32(ops[1])

		sample(op1, op2, cmd.name)
			
		dut.exu2ialu_main_op1_i.value = op1
		dut.exu2ialu_main_op2_i.value = op2

		await Timer(1, units="step")
		res = Int32(dut.ialu2exu_main_res_o.value)	

		assert check_result(cmd, op1, op2, res), \
				'Failed test #' + str(i) + ': output is incorrect!'

def check_result(cmd, op1, op2, res):
	if (cmd == Cmd.ADD):
		correct = (res == op1+op2)
	elif (cmd == Cmd.SUB):
		correct = (res == op1-op2)
	else: 
		assert False

	return correct
	