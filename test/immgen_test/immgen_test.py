#cocotb test immgen 

import cocotb
from cocotb.triggers import Timer

@cocotb.test()
async def test_Itype(dut):
    """Test I-type instruction"""
    # assgin a I-type instruction with random immediate value and set rs1 func3 rd opcode all 0 
    # since we only test immgen
    # rs1 in I-type instruction is 19-15
    # func3 in I-type instruction is 14-12
    # rd in I-type instruction is 11-7
    # opcode in I-type instruction is 6-0

    dut.instruction.value = 0

    dut.instruction.value = dut.instruction.value | (0xAAA << 20)

    dut.imm_select.value = 0x0
    await Timer(1, units='ns')

    expected_val = 0xFFFFFAAA
    assert dut.imm.value == expected_val, (
        f"imm={dut.imm.value}, expected={hex(expected_val)}"
    )

@cocotb.test()
async def test_Btype(dut):
    """Test B-type instruction"""

    dut.instruction.value = 0

    dut.instruction.value = dut.instruction.value | 0xFE000F80

    dut.imm_select.value = 0x2
    await Timer(1, units='ns')

    expected_val = 0xFFFFFFFE
    assert dut.imm.value == expected_val, (
        f"imm={dut.imm.value}, expected={hex(expected_val)}"
    )

@cocotb.test()
async def test_Stype(dut):
    """Test S-type instruction"""

    dut.instruction.value = 0

    dut.instruction.value = dut.instruction.value | 0xFE000F80
    dut.imm_select.value = 0x1

    await Timer(1, units='ns')

    expected_val = 0xFFFFFFFF
    assert dut.imm.value == expected_val, (
        f"imm={dut.imm.value}, expected={hex(expected_val)}"
    )

@cocotb.test()
async def test_Jtype(dut):
    """Test J-type instruction"""

    dut.instruction.value = 0

    dut.instruction.value = dut.instruction.value | 0xFFFFF000
    dut.imm_select.value = 0x3

    await Timer(1, units='ns')

    expected_val = 0xFFFFFFFE
    assert dut.imm.value == expected_val, (
        f"imm={dut.imm.value}, expected={hex(expected_val)}"
    )

@cocotb.test()
async def test_Utype(dut):
    """Test U-type instruction"""

    dut.instruction.value = 0

    dut.instruction.value = dut.instruction.value | 0xFFFFF000
    dut.imm_select.value = 0x4

    await Timer(1, units='ns')

    expected_val = 0xFFFFF000
    assert dut.imm.value == expected_val, (
        f"imm={dut.imm.value}, expected={hex(expected_val)}"
    )