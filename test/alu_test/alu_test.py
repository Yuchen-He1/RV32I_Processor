# cocotb test for alu

import cocotb
from cocotb.triggers import Timer
# alu_control is a 4-bit control signal
# 0000-add, 0001-sub, 0010-and, 0011-or, 0100-xor, 0101-nor,
# 0110-sll, 0111-srl, 1000-sra, 1001-slt, 1010-sltu
@cocotb.test()
async def test_alu_add(dut):
    """Test ALU ADD operation"""
    # Set inputs
    dut.alu_control.value = 0
    dut.a.value = 5
    dut.b.value = 3
    await Timer(1, units='ns')
    # Check output
    expected_val = 8
    assert dut.result.value == expected_val, (
        f"result={dut.result.value}, expected={expected_val}"
    )

@cocotb.test()
async def test_alu_sub(dut):
    """Test ALU SUB operation"""
    # Set inputs
    dut.alu_control.value = 1
    dut.a.value = 5
    dut.b.value = 3
    await Timer(1, units='ns')
    # Check output
    expected_val = 2
    assert dut.result.value == expected_val, (
        f"result={dut.result.value}, expected={expected_val}"
    )

@cocotb.test()
async def test_alu_and(dut):
    """Test ALU AND operation"""
    # Set inputs
    dut.alu_control.value = 2
    dut.a.value = 5
    dut.b.value = 3
    await Timer(1, units='ns')
    # Check output
    expected_val = 1
    assert dut.result.value == expected_val, (
        f"result={dut.result.value}, expected={expected_val}"
    )

@cocotb.test()
async def test_alu_or(dut):
    """Test ALU OR operation"""
    # Set inputs
    dut.alu_control.value = 3
    dut.a.value = 5
    dut.b.value = 3
    await Timer(1, units='ns')
    # Check output
    expected_val = 7
    dut._log.info(f"result={hex(dut.result.value)}, expected={hex(expected_val)}")
    assert dut.result.value == expected_val, (
        f"result={dut.result.value}, expected={expected_val}"
    )

@cocotb.test()
async def test_alu_xor(dut):
    """Test ALU XOR operation"""
    # Set inputs
    dut.alu_control.value = 4
    dut.a.value = 5
    dut.b.value = 3
    await Timer(1, units='ns')
    # Check output
    expected_val = 6
    dut._log.info(f"result={dut.result.value}, expected={hex(expected_val)}")
    assert dut.result.value == expected_val, (
        f"result={dut.result.value}, expected={expected_val}"
    )

@cocotb.test()
async def test_alu_nor(dut):
    """Test ALU NOR operation"""
    # Set inputs
    dut.alu_control.value = 5
    dut.a.value = 5
    dut.b.value = 3
    await Timer(1, units='ns')
    # Check output
    #-8 2's complement
    expected_val = '11111111111111111111111111111000' 
    assert dut.result.value == expected_val, (
        f"result={dut.result.value}, expected={expected_val}"
    )

@cocotb.test()
async def test_alu_sll(dut):
    """Test ALU SLL operation"""
    # Set inputs
    dut.alu_control.value = 6
    dut.a.value = 5
    dut.b.value = 1
    await Timer(1, units='ns')
    # Check output
    expected_val = 10
    assert dut.result.value == expected_val, (
        f"result={dut.result.value}, expected={expected_val}"
    )

@cocotb.test()
async def test_alu_srl(dut):
    """Test ALU SRL operation"""
    # Set inputs
    dut.alu_control.value = 7
    dut.a.value = 5
    dut.b.value = 1
    await Timer(1, units='ns')
    # Check output
    expected_val = 2
    assert dut.result.value == expected_val, (
        f"result={dut.result.value}, expected={expected_val}"
    )

@cocotb.test()
async def test_alu_sra(dut):
    """Test ALU SRA operation"""
    # Set inputs
    dut.alu_control.value = 8
    dut.a.value = -5
    dut.b.value = 1
    await Timer(1, units='ns')
    # Check output
    expected_val = '11111111111111111111111111111101'
    assert dut.result.value == expected_val, (
        f"result={dut.result.value}, expected={expected_val}"
    )

@cocotb.test()
async def test_alu_slt1(dut):
    """Test ALU SLT operation"""
    # Set inputs
    dut.alu_control.value = 9
    dut.a.value = 5
    dut.b.value = 3
    await Timer(1, units='ns')
    # Check output
    expected_val = 0
    assert dut.result.value == expected_val, (
        f"result={dut.result.value}, expected={expected_val}"
    )
@cocotb.test()
async def test_alu_slt2(dut):
    """Test ALU SLT operation"""
    # Set inputs
    dut.alu_control.value = 9
    dut.a.value = 3
    dut.b.value = 5
    await Timer(1, units='ns')
    # Check output
    expected_val = 0x1
    assert dut.result.value == expected_val, (
        f"result={dut.result.value}, expected={expected_val}"
    )
@cocotb.test()
async def test_alu_sltu1(dut):
    """Test ALU SLTU operation"""
    # Set inputs
    dut.alu_control.value = 10
    dut.a.value = 3
    dut.b.value = 5
    await Timer(1, units='ns')
    # Check output
    expected_val = 0x1
    assert dut.result.value == expected_val, (
        f"result={dut.result.value}, expected={expected_val}"
    )
@cocotb.test()
async def test_alu_sltu2(dut):
    """Test ALU SLTU operation"""
    # Set inputs
    dut.alu_control.value = 10
    dut.a.value = 5
    dut.b.value = 3
    await Timer(1, units='ns')
    # Check output
    expected_val = 0
    assert dut.result.value == expected_val, (
        f"result={dut.result.value}, expected={expected_val}"
    )
# Add more tests as needed for other ALU operations