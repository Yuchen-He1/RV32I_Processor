# Simple cocotb test for RISC-V datapath
import os
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, ClockCycles

# Generate instruction memory content
def generate_test_program():
    """Generate a simple test program focusing on R-type instructions"""
    with open("instructions.txt", "w") as f:
        # R-type instruction test
        f.write("00a00093\n")  # addi x1, x0, 10    # x1 = 10
        f.write("00500113\n")  # addi x2, x0, 5     # x2 = 5
        f.write("001081b3\n")  # add  x3, x1, x2    # x3 = x1 + x2 = 15
        f.write("40208233\n")  # sub  x4, x1, x2    # x4 = x1 - x2 = 5
        f.write("0020f2b3\n")  # and  x5, x1, x2    # x5 = x1 & x2 = 0
        f.write("0020e333\n")  # or   x6, x1, x2    # x6 = x1 | x2 = 15
        f.write("0020c3b3\n")  # xor  x7, x1, x2    # x7 = x1 ^ x2 = 15
        f.write("00209433\n")  # sll  x8, x1, x2    # x8 = x1 << x2 = 320
        f.write("00a00093\n")  # addi x1, x0, 10    # Reset x1 = 10 (to check against PC)

@cocotb.test()
async def test_datapath_simple(dut):
    """Test basic datapath functionality with R-type instructions"""
    # Generate the test program
    generate_test_program()
    
    # Clock setup
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Reset the processor
    dut.rst.value = 1
    await ClockCycles(dut.clk, 2)
    dut.rst.value = 0
    
    # Run for 10 cycles to execute all instructions (9 instructions + 1 cycle buffer)
    for i in range(10):
        # Get register values before executing instruction for debug
        if i > 0:
            try:
                reg1 = int(dut.reg_file_inst.registers[1].value)
                reg2 = int(dut.reg_file_inst.registers[2].value)
                reg3 = int(dut.reg_file_inst.registers[3].value) if i > 2 else "N/A"
                dut._log.info(f"Before cycle {i}: x1={reg1}, x2={reg2}, x3={reg3}")
            except Exception:
                pass
                
        # Get current PC and instruction
        pc_val = int(dut.PC.value)
        instr_val = int(dut.instruction.value)
        dut._log.info(f"Cycle {i}: PC = {pc_val}, Instruction = 0x{instr_val:08x}")
        
        # Print ALU inputs for debugging
        if i > 1:  # After first two addi instructions
            try:
                a_val = int(dut.alu_inst.a.value)
                b_val = int(dut.alu_inst.b.value)
                alu_control = int(dut.alu_inst.alu_control.value)
                dut._log.info(f"ALU inputs: a={a_val}, b={b_val}, alu_control={alu_control}")
            except Exception:
                pass
        
        # Execute one cycle
        await RisingEdge(dut.clk)
    
    # Check register values after execution
    try:
        # Check register x1 (should be 10)
        reg1_val = int(dut.reg_file_inst.registers[1].value)
        dut._log.info(f"Final x1 = {reg1_val}, Expected: 10")
        assert reg1_val == 10, f"x1 should be 10, got {reg1_val}"
        
        # Check register x2 (should be 5)
        reg2_val = int(dut.reg_file_inst.registers[2].value)
        dut._log.info(f"Final x2 = {reg2_val}, Expected: 5")
        assert reg2_val == 5, f"x2 should be 5, got {reg2_val}"
        
        # Check register x3 (add result: should be 15)
        reg3_val = int(dut.reg_file_inst.registers[3].value)
        dut._log.info(f"Final x3 = {reg3_val}, Expected: 15")
        assert reg3_val == 15, f"x3 should be 15, got {reg3_val}"
        
        # Check register x4 (sub result: should be 5)
        reg4_val = int(dut.reg_file_inst.registers[4].value)
        dut._log.info(f"Final x4 = {reg4_val}, Expected: 5")
        assert reg4_val == 5, f"x4 should be 5, got {reg4_val}"
        
        # Check register x5 (and result: should be 0)
        reg5_val = int(dut.reg_file_inst.registers[5].value)
        dut._log.info(f"Final x5 = {reg5_val}, Expected: 0")
        assert reg5_val == 0, f"x5 should be 0, got {reg5_val}"
        
        # Check register x6 (or result: should be 15)
        reg6_val = int(dut.reg_file_inst.registers[6].value)
        dut._log.info(f"Final x6 = {reg6_val}, Expected: 15")
        assert reg6_val == 15, f"x6 should be 15, got {reg6_val}"
        
        # Check register x7 (xor result: should be 15)
        reg7_val = int(dut.reg_file_inst.registers[7].value)
        dut._log.info(f"Final x7 = {reg7_val}, Expected: 15")
        assert reg7_val == 15, f"x7 should be 15, got {reg7_val}"
        
        # Check register x8 (sll result: should be 320)
        reg8_val = int(dut.reg_file_inst.registers[8].value)
        dut._log.info(f"Final x8 = {reg8_val}, Expected: 320")
        assert reg8_val == 320, f"x8 should be 320, got {reg8_val}"
        
    except Exception as e:
        dut._log.error(f"Test failed: {str(e)}")
        assert False, f"Test failed: {str(e)}"
    
    dut._log.info("R-type instruction test passed!")