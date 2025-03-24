# # Simple cocotb test for RISC-V datapath
# import os
# import cocotb
# from cocotb.clock import Clock
# from cocotb.triggers import Timer, RisingEdge, ClockCycles

# # Generate instruction memory content
# def generate_test_program():
#     """Generate test program from provided hexadecimal instructions"""
#     with open("instructions.txt", "w") as f:
#         # Initialize registers with known values - simple R-type test
#         f.write("00a00093\n")  # addi x1, x0, 10    # x1 = 10
#         f.write("00500113\n")  # addi x2, x0, 5     # x2 = 5
#         f.write("002081b3\n")  # add x3, x1, x2     # x3 = x1 + x2 = 15
#         f.write("40208233\n")  # sub x4, x1, x2     # x4 = x1 - x2 = 5

#         # Previous program (commented out)
#         # f.write("00600613\n")
#         # f.write("014000ef\n")
#         # f.write("40000613\n")
#         # f.write("00361613\n")
#         # f.write("00a62023\n")
#         # f.write("00000073\n")
#         # f.write("ff010113\n")
#         # f.write("00112623\n")
#         # f.write("00812423\n")
#         # f.write("00912223\n")
#         # f.write("01212023\n")
#         # f.write("00c00433\n")
#         # f.write("00200293\n")
#         # f.write("02544263\n")
#         # f.write("fff40613\n")
#         # f.write("fddff0ef\n")
#         # f.write("00a004b3\n")
#         # f.write("ffe40613\n")
#         # f.write("fd1ff0ef\n")
#         # f.write("00a00933\n")
#         # f.write("01248533\n")
#         # f.write("0080006f\n")
#         # f.write("00100513\n")
#         # f.write("00c12083\n")
#         # f.write("00812403\n")
#         # f.write("00412483\n")
#         # f.write("00012903\n")
#         # f.write("01010113\n")
#         # f.write("00008067\n")

# @cocotb.test()
# async def test_datapath_simple(dut):
#     """Test datapath functionality with simple R-type instructions"""
#     # Generate the test program
#     generate_test_program()
    
#     # Clock setup
#     clock = Clock(dut.clk, 10, units="ns")
#     cocotb.start_soon(clock.start())
    
#     # Reset the processor
#     dut.rst.value = 1
#     await ClockCycles(dut.clk, 2)
#     dut.rst.value = 0
    
#     # Run for 10 cycles (enough for our 4 instructions)
#     for i in range(4):
#         # Get current PC and instruction
#         await RisingEdge(dut.clk)
#         pc_val = int(dut.PC.value)
#         instr_val = int(dut.instruction.value)
#         dut._log.info(f"===== Cycle {i}: PC = 0x{pc_val:08x}, Instruction = 0x{instr_val:08x} =====")
        
#         # ------ Print PC and Next PC information ------
#         try:
#             pc_current = int(dut.pc_current.value)
#             pc_plus_4 = int(dut.pc_plus_4.value)
#             pc_next = int(dut.pc_next.value)
#             dut._log.info(f"PC: current=0x{pc_current:08x}, plus_4=0x{pc_plus_4:08x}, next=0x{pc_next:08x}")
#         except Exception as e:
#             dut._log.warning(f"Error reading PC signals: {e}")
            
#         # ------ Print Instruction Memory output ------
#         try:
#             instruction = int(dut.instruction.value)
#             dut._log.info(f"IMEM: instruction=0x{instruction:08x}")
#             # Decode instruction for better readability
#             opcode = instruction & 0x7F
#             rd = (instruction >> 7) & 0x1F
#             funct3 = (instruction >> 12) & 0x7
#             rs1 = (instruction >> 15) & 0x1F
#             rs2 = (instruction >> 20) & 0x1F
#             funct7 = (instruction >> 25) & 0x7F
#             dut._log.info(f"  Decoded: opcode=0x{opcode:02x}, rd=x{rd}, funct3=0x{funct3:x}, rs1=x{rs1}, rs2=x{rs2}, funct7=0x{funct7:02x}")
#         except Exception as e:
#             dut._log.warning(f"Error reading instruction: {e}")
        
#         # ------ Print Control Logic signals ------
#         try:
#             pcsel = int(dut.control_logic_inst.pcsel.value)
#             alu_op = int(dut.control_logic_inst.alu_op.value)
#             operand1_sel = int(dut.control_logic_inst.operand1_sel.value)
#             operand2_sel = int(dut.control_logic_inst.operand2_sel.value)
#             reg_write = int(dut.control_logic_inst.reg_write.value)
#             immgen_sel = int(dut.control_logic_inst.immgen_sel.value)
#             dmem_write = int(dut.control_logic_inst.dmem_write.value)
#             dmem_read = int(dut.control_logic_inst.dmem_read.value)
#             brunsigned = int(dut.control_logic_inst.brunsigned.value)
#             writeback_sel = int(dut.control_logic_inst.writeback_sel.value)
            
#             dut._log.info(f"Control Logic: pcsel={pcsel}, alu_op=0x{alu_op:x}, op1_sel={operand1_sel}, op2_sel={operand2_sel}")
#             dut._log.info(f"  reg_write={reg_write}, immgen_sel={immgen_sel}, dmem_write={dmem_write}, dmem_read={dmem_read}")
#             dut._log.info(f"  brunsigned={brunsigned}, writeback_sel={writeback_sel}")
#         except Exception as e:
#             dut._log.warning(f"Error reading control signals: {e}")
            
#         # ------ Print Immediate Generator output ------
#         try:
#             imm = int(dut.immgen_inst.imm.value)
#             dut._log.info(f"ImmGen: imm=0x{imm:08x} ({imm})")
#         except Exception as e:
#             dut._log.warning(f"Error reading immediate: {e}")
            
#         # ------ Print Register File signals ------
#         try:
#             rs1_addr = int(dut.reg_file_inst.rs1_addr.value)
#             rs2_addr = int(dut.reg_file_inst.rs2_addr.value)
#             rd_addr = int(dut.reg_file_inst.rd_addr.value)
#             rs1_data = int(dut.reg_file_inst.rs1_data.value)
#             rs2_data = int(dut.reg_file_inst.rs2_data.value)
#             rd_data = int(dut.reg_file_inst.rd_data.value)
            
#             dut._log.info(f"RegFile: rs1_addr=x{rs1_addr}, rs2_addr=x{rs2_addr}, rd_addr=x{rd_addr}")
#             dut._log.info(f"  rs1_data=0x{rs1_data:08x} ({rs1_data}), rs2_data=0x{rs2_data:08x} ({rs2_data})")
#             dut._log.info(f"  rd_data=0x{rd_data:08x} ({rd_data}), reg_write={reg_write}")
            
#             # Print all registers for debugging
#             dut._log.info(f"  All registers:")
#             for reg_idx in range(1, 16):  # Print registers x1-x15
#                 try:
#                     reg_val = int(dut.reg_file_inst.registers[reg_idx].value)
#                     dut._log.info(f"    x{reg_idx} = {reg_val}")
#                 except:
#                     pass
#         except Exception as e:
#             dut._log.warning(f"Error reading register file: {e}")
            
#         # ------ Print Branch Comparator signals ------
#         try:
#             breq = int(dut.branch_comparator.breq.value)
#             brlt = int(dut.branch_comparator.brlt.value)
#             dut._log.info(f"Branch Comparator: breq={breq}, brlt={brlt}, brunsigned={brunsigned}")
#         except Exception as e:
#             dut._log.warning(f"Error reading branch comparator: {e}")
            
#         # ------ Print ALU Mux signals ------
#         try:
#             alu_operand1 = int(dut.alu_operand1.value)
#             alu_operand2 = int(dut.alu_operand2.value)
#             dut._log.info(f"ALU Muxes: operand1=0x{alu_operand1:08x} ({alu_operand1}), operand2=0x{alu_operand2:08x} ({alu_operand2})")
#         except Exception as e:
#             dut._log.warning(f"Error reading ALU muxes: {e}")
            
#         # ------ Print ALU signals ------
#         try:
#             alu_a = int(dut.alu_inst.a.value)
#             alu_b = int(dut.alu_inst.b.value)
#             alu_control = int(dut.alu_inst.alu_control.value)
#             alu_result = int(dut.alu_inst.result.value)
#             dut._log.info(f"ALU: a=0x{alu_a:08x} ({alu_a}), b=0x{alu_b:08x} ({alu_b})")
#             dut._log.info(f"  control=0x{alu_control:x}, result=0x{alu_result:08x} ({alu_result})")
#         except Exception as e:
#             dut._log.warning(f"Error reading ALU signals: {e}")
            
#         # ------ Print Data Memory signals ------
#         try:
#             dmem_addr = int(dut.dmem_inst.addr.value)
#             dmem_input_data = int(dut.dmem_inst.input_data.value)
#             dmem_output_data = int(dut.dmem_inst.output_data.value)
#             dut._log.info(f"DMEM: addr=0x{dmem_addr:08x}, input_data=0x{dmem_input_data:08x}")
#             dut._log.info(f"  output_data=0x{dmem_output_data:08x}, store={dmem_write}, load={dmem_read}")
#         except Exception as e:
#             dut._log.warning(f"Error reading data memory: {e}")
            
#         # ------ Print Writeback Mux signals ------
#         try:
#             wb_a = int(dut.writeback_mux.a.value)
#             wb_b = int(dut.writeback_mux.b.value)
#             wb_c = int(dut.writeback_mux.c.value)
#             wb_d = int(dut.writeback_mux.d.value)
#             wb_out = int(dut.writeback_mux.out.value)
#             dut._log.info(f"Writeback Mux: a=0x{wb_a:08x}, b=0x{wb_b:08x}, c=0x{wb_c:08x}, d=0x{wb_d:08x}")
#             dut._log.info(f"  sel={writeback_sel}, out=0x{wb_out:08x} ({wb_out})")
#         except Exception as e:
#             dut._log.warning(f"Error reading writeback mux: {e}")
        
#         # Execute one cycle
#         await RisingEdge(dut.clk)
    
#     # Final register check
#     try:
#         # Check register x1 (should be 10)
#         reg1_val = int(dut.reg_file_inst.registers[1].value)
#         dut._log.info(f"Final x1 = {reg1_val}, Expected: 10")
#         assert reg1_val == 10, f"x1 should be 10, got {reg1_val}"
        
#         # Check register x2 (should be 5)
#         reg2_val = int(dut.reg_file_inst.registers[2].value)
#         dut._log.info(f"Final x2 = {reg2_val}, Expected: 5")
#         assert reg2_val == 5, f"x2 should be 5, got {reg2_val}"
        
#         # Check register x3 (add result: should be 15)
#         reg3_val = int(dut.reg_file_inst.registers[3].value)
#         dut._log.info(f"Final x3 = {reg3_val}, Expected: 15")
#         assert reg3_val == 15, f"x3 should be 15, got {reg3_val}"
        
#         # Check register x4 (sub result: should be 5)
#         reg4_val = int(dut.reg_file_inst.registers[4].value)
#         dut._log.info(f"Final x4 = {reg4_val}, Expected: 5")
#         assert reg4_val == 5, f"x4 should be 5, got {reg4_val}"
#     except Exception as e:
#         dut._log.error(f"Test failed: {str(e)}")
#         assert False, f"Test failed: {str(e)}"
    
#     dut._log.info("Test completed - check logs for execution trace")



# Simple cocotb test for RISC-V datapath
import os
import cocotb
from cocotb.clock import Clock
from cocotb.triggers import Timer, RisingEdge, ClockCycles

# Generate instruction memory content
def generate_test_program():
    """Generate test program from provided hexadecimal instructions"""
    with open("instructions.txt", "w") as f:
        # Initialize registers with known values - simple R-type test
        f.write("00a00093\n")  # addi x1, x0, 10    # x1 = 10
        f.write("00500113\n")  # addi x2, x0, 5     # x2 = 5
        f.write("002081b3\n")  # add x3, x1, x2     # x3 = x1 + x2 = 15
        f.write("40208233\n")  # sub x4, x1, x2     # x4 = x1 - x2 = 5
        f.write("00000013\n")  # nop
    return 5
# Generate program for branch instruction test
def generate_branch_program():
    """Generate a simple program to test branch instructions"""
    with open("instructions.txt", "w") as f:
        # Setup register initial values
        f.write("00a00093\n")  # addi x1, x0, 10    # x1 = 10
        f.write("00a00113\n")  # addi x2, x0, 10    # x2 = 10
        f.write("00000193\n")  # addi x3, x0, 0     # x3 = 0 (branch target counter)
        
        # Test BEQ (should branch)
        f.write("00208463\n")  # beq x1, x2, label1 # branch if x1 == x2 (should branch)
        f.write("00000013\n")  # nop                # should be skipped
        
        # label1: (PC + 8)
        f.write("00118193\n")  # addi x3, x3, 1     # x3 += 1 (executed after branch)
        f.write("00000013\n")  # nop                # padding at the end
    return 8
        # Total program length: 8 instructions
        
# Generate program for memory operations test
def generate_memory_program():
    """Generate a simple program to test memory operations"""
    with open("instructions.txt", "w") as f:
        # Setup register initial values
        f.write("00a00093\n")  # addi x1, x0, 10     # x1 = 10 (data to store)
        f.write("01000113\n")  # addi x2, x0, 16     # x2 = 16 (memory address)
        
        # Store word (x1) to address in x2
        f.write("00112023\n")  # sw x1, 0(x2)        # mem[16] = 10
        
        # Load word from memory into x3
        f.write("00012183\n")  # lw x3, 0(x2)        # x3 = mem[16] (should be 10)
        f.write("00000013\n")  # nop                 # padding at the end
    return 5    
        # Total program length: 5 instructions

# Generate program for jump instruction test
def generate_jump_program():
    """Generate a simple program to test jump instructions"""
    with open("instructions.txt", "w") as f:
        # Setup registers
        f.write("00000093\n")  # addi x1, x0, 0      # x1 = 0 (will be overwritten by JAL)
        
        # Test JAL (jump and link)
        f.write("00c000ef\n")  # jal x1, offset12    # jump to PC+12, x1 = PC+4
        
        # Instructions that should be skipped
        f.write("00000013\n")  # nop
        f.write("00000013\n")  # nop
        
        # Label (PC + 12)
        f.write("00100113\n")  # addi x2, x0, 1      # x2 = 1 (executed after jump)
        f.write("00000013\n")  # nop                 # padding at the end
    return 6
    
def generate_custom_program():
    """Generate the provided custom program"""
    with open("instructions.txt", "w") as f:
        # Write the provided instruction sequence
        f.write("00600613\n")
        f.write("014000ef\n")
        f.write("40000613\n")
        f.write("00361613\n")
        f.write("00a62023\n")
        f.write("00000073\n")
        f.write("ff010113\n")
        f.write("00112623\n")
        f.write("00812423\n")
        f.write("00912223\n")
        f.write("01212023\n")
        f.write("00c00433\n")
        f.write("00200293\n")
        f.write("02544263\n")
        f.write("fff40613\n")
        f.write("fddff0ef\n")
        f.write("00a004b3\n")
        f.write("ffe40613\n")
        f.write("fd1ff0ef\n")
        f.write("00a00933\n")
        f.write("01248533\n")
        f.write("0080006f\n")
        f.write("00100513\n")
        f.write("00c12083\n")
        f.write("00812403\n")
        f.write("00412483\n")
        f.write("00012903\n")
        f.write("01010113\n")
        f.write("00008067\n")
        
    # Total program length: 29 instructions
    return 29
@cocotb.test()
async def test_datapath_simple(dut):
    """Test datapath functionality with simple R-type instructions"""
    # Generate the test program
    #generate_test_program()
    #len=generate_branch_program()
    #len=generate_memory_program()
    #len=generate_jump_program()
    len=generate_custom_program()
    # Clock setup
    clock = Clock(dut.clk, 10, units="ns")
    cocotb.start_soon(clock.start())
    
    # Reset the processor
    dut.rst.value = 1
    await ClockCycles(dut.clk, 2)
    dut.rst.value = 0
    
    # Run for 10 cycles (enough for our 4 instructions)
    for i in range(464):
        # Get current PC and instruction
        await RisingEdge(dut.clk)
        pc_val = int(dut.PC.value)
        instr_val = int(dut.instruction.value)
        dut._log.info(f"\n\n===== Cycle {i}: PC = 0x{pc_val:08x}, Instruction = 0x{instr_val:08x} =====")
        
        # ------ Print PC and PC-related signals ------
        try:
            pc_current = int(dut.pc_current.value)
            pc_plus_4 = int(dut.pc_plus_4.value)
            pc_next = int(dut.pc_next.value)
            dut._log.info(f"\nPC Register:")
            dut._log.info(f"  current=0x{pc_current:08x}")
            dut._log.info(f"  plus_4=0x{pc_plus_4:08x}")
            dut._log.info(f"  next=0x{pc_next:08x}")
            
            # # Analyze PC value sequence
            # expected_pc = i * 4
            # if pc_val != expected_pc:
            #     dut._log.warning(f"  PC Sequence Issue: PC value is 0x{pc_val:08x}, expected 0x{expected_pc:08x}")
            #     dut._log.warning(f"  PC Difference: {pc_val - expected_pc} bytes")
        except Exception as e:
            dut._log.warning(f"\nError reading PC signals: {e}")
            
        # ------ Print Instruction Memory (Imem) output ------
        try:
            instruction = int(dut.instruction.value)
            dut._log.info(f"\nImem:")
            dut._log.info(f"  instruction=0x{instruction:08x}")
            
            # Decode instruction for better readability
            opcode = instruction & 0x7F
            rd = (instruction >> 7) & 0x1F
            funct3 = (instruction >> 12) & 0x7
            rs1 = (instruction >> 15) & 0x1F
            rs2 = (instruction >> 20) & 0x1F
            funct7 = (instruction >> 25) & 0x7F
            dut._log.info(f"  Decoded:")
            dut._log.info(f"    opcode=0x{opcode:02x}")
            dut._log.info(f"    rd=x{rd}")
            dut._log.info(f"    funct3=0x{funct3:x}")
            dut._log.info(f"    rs1=x{rs1}")
            dut._log.info(f"    rs2=x{rs2}")
            dut._log.info(f"    funct7=0x{funct7:02x}")
        except Exception as e:
            dut._log.warning(f"\nError reading Imem: {e}")
        
        # ------ Print Control Logic signals ------
        try:
            pcsel = int(dut.control_logic_inst.pcsel.value)
            alu_op = int(dut.control_logic_inst.alu_op.value)
            operand1_sel = int(dut.control_logic_inst.operand1_sel.value)
            operand2_sel = int(dut.control_logic_inst.operand2_sel.value)
            reg_write = int(dut.control_logic_inst.reg_write.value)
            immgen_sel = int(dut.control_logic_inst.immgen_sel.value)
            dmem_write = int(dut.control_logic_inst.dmem_write.value)
            dmem_read = int(dut.control_logic_inst.dmem_read.value)
            brunsigned = int(dut.control_logic_inst.brunsigned.value)
            writeback_sel = int(dut.control_logic_inst.writeback_sel.value)
            
            dut._log.info(f"\ncontrol_logic_inst:")
            dut._log.info(f"  pcsel={pcsel}")
            dut._log.info(f"  alu_op=0x{alu_op:x}")
            dut._log.info(f"  operand1_sel={operand1_sel}")
            dut._log.info(f"  operand2_sel={operand2_sel}")
            dut._log.info(f"  reg_write={reg_write}")
            dut._log.info(f"  immgen_sel={immgen_sel}")
            dut._log.info(f"  dmem_write={dmem_write}")
            dut._log.info(f"  dmem_read={dmem_read}")
            dut._log.info(f"  brunsigned={brunsigned}")
            dut._log.info(f"  writeback_sel={writeback_sel}")
        except Exception as e:
            dut._log.warning(f"\nError reading control_logic_inst: {e}")
            
        # ------ Print Immediate Generator output ------
        try:
            imm = int(dut.immgen_inst.imm.value)
            dut._log.info(f"\nimmgen_inst:")
            dut._log.info(f"  imm=0x{imm:08x} ({imm})")
        except Exception as e:
            dut._log.warning(f"\nError reading immgen_inst: {e}")
            
        # ------ Print Register File signals ------
        try:
            rs1_addr = int(dut.reg_file_inst.rs1_addr.value)
            rs2_addr = int(dut.reg_file_inst.rs2_addr.value)
            rd_addr = int(dut.reg_file_inst.rd_addr.value)
            rs1_data = int(dut.reg_file_inst.rs1_data.value)
            rs2_data = int(dut.reg_file_inst.rs2_data.value)
            rd_data = int(dut.reg_file_inst.rd_data.value)
            
            dut._log.info(f"\nreg_file_inst:")
            dut._log.info(f"  rs1_addr=x{rs1_addr}")
            dut._log.info(f"  rs2_addr=x{rs2_addr}")
            dut._log.info(f"  rd_addr=x{rd_addr}")
            dut._log.info(f"  rs1_data=0x{rs1_data:08x} ({rs1_data})")
            dut._log.info(f"  rs2_data=0x{rs2_data:08x} ({rs2_data})")
            dut._log.info(f"  rd_data=0x{rd_data:08x} ({rd_data})")
            dut._log.info(f"  reg_write={reg_write}")
            
            # Print all registers for debugging
            dut._log.info(f"  Registers:")
            for reg_idx in range(0, 16):  # Print registers x0-x15
                try:
                    reg_val = int(dut.reg_file_inst.registers[reg_idx].value)
                    dut._log.info(f"    x{reg_idx} = {reg_val}")
                except:
                    dut._log.info(f"    x{reg_idx} = not accessible")
        except Exception as e:
            dut._log.warning(f"\nError reading reg_file_inst: {e}")
            
        # ------ Print Branch Comparator signals ------
        try:
            breq = int(dut.branch_comparator.breq.value)
            brlt = int(dut.branch_comparator.brlt.value)
            dut._log.info(f"\nbranch_comparator:")
            dut._log.info(f"  breq={breq}")
            dut._log.info(f"  brlt={brlt}")
            dut._log.info(f"  brunsigned={brunsigned}")
        except Exception as e:
            dut._log.warning(f"\nError reading branch_comparator: {e}")
            
        # ------ Print ALU Mux signals ------
        try:
            alu_operand1 = int(dut.alu_operand1.value)
            alu_operand2 = int(dut.alu_operand2.value)
            dut._log.info(f"\nALU operands (mux outputs):")
            dut._log.info(f"  alu_operand1=0x{alu_operand1:08x} ({alu_operand1})")
            dut._log.info(f"  alu_operand2=0x{alu_operand2:08x} ({alu_operand2})")
        except Exception as e:
            dut._log.warning(f"\nError reading ALU operands: {e}")
            
        # ------ Print ALU signals ------
        try:
            alu_a = int(dut.alu_inst.a.value)
            alu_b = int(dut.alu_inst.b.value)
            alu_control = int(dut.alu_inst.alu_control.value)
            alu_result = int(dut.alu_inst.result.value)
            dut._log.info(f"\nalu_inst:")
            dut._log.info(f"  a=0x{alu_a:08x} ({alu_a})")
            dut._log.info(f"  b=0x{alu_b:08x} ({alu_b})")
            dut._log.info(f"  alu_control=0x{alu_control:x}")
            dut._log.info(f"  result=0x{alu_result:08x} ({alu_result})")
        except Exception as e:
            dut._log.warning(f"\nError reading alu_inst: {e}")
            
        # ------ Print Data Memory signals ------
        try:
            dmem_addr = int(dut.dmem_inst.addr.value)
            dmem_input_data = int(dut.dmem_inst.input_data.value)
            dmem_output_data = int(dut.dmem_inst.output_data.value)
            dut._log.info(f"\ndmem_inst:")
            dut._log.info(f"  addr=0x{dmem_addr:08x}")
            dut._log.info(f"  input_data=0x{dmem_input_data:08x}")
            dut._log.info(f"  output_data=0x{dmem_output_data:08x}")
            dut._log.info(f"  store={dmem_write}")
            dut._log.info(f"  load={dmem_read}")
        except Exception as e:
            dut._log.warning(f"\nError reading dmem_inst: {e}")
            
        # ------ Print Writeback Mux signals ------
        try:
            wb_a = int(dut.writeback_mux.a.value)
            wb_b = int(dut.writeback_mux.b.value)
            wb_c = int(dut.writeback_mux.c.value)
            wb_d = int(dut.writeback_mux.d.value)
            wb_out = int(dut.writeback_mux.out.value)
            dut._log.info(f"\nwriteback_mux:")
            dut._log.info(f"  a=0x{wb_a:08x} (PC+4)")
            dut._log.info(f"  b=0x{wb_b:08x} (DMEM data)")
            dut._log.info(f"  c=0x{wb_c:08x} (ALU result)")
            dut._log.info(f"  d=0x{wb_d:08x} (unused)")
            dut._log.info(f"  sel={writeback_sel}")
            dut._log.info(f"  out=0x{wb_out:08x} ({wb_out})")
        except Exception as e:
            dut._log.warning(f"\nError reading writeback_mux: {e}")
    # Add one more clock cycle to allow register writes to complete
    await RisingEdge(dut.clk)










