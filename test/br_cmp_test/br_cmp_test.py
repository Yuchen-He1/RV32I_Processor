# cocotb test for br_cmp

import cocotb 
from cocotb.triggers import Timer

@cocotb.test()
async def test_br_cmp_signed(dut):
    """Test Branch Comparator"""
    # Set inputs
    dut.rs1.value = 0b11111111111111111111111111111101
    dut.rs2.value = 0b11111111111111111111111111111000
    dut.unsigned_cmp = 0
    await Timer(1, units='ns')
    # Check output
    expected_val_1 = 0
    assert dut.breq.value == expected_val_1, (
        f"br_cmp={dut.breq.value}, expected={expected_val_1}"
    )
    expected_val_2 = 0
    assert dut.brlt.value == expected_val_2, (
        f"br_cmp={dut.brlt.value}, expected={expected_val_2}"
    )

@cocotb.test()
async def test_br_cmp_unsigned(dut):
    """Test Branch Comparator"""
    # Set inputs
    dut.rs1.value = 0b01111111111111111111111111111111
    dut.rs2.value = 0b11111111111111111111111111111111
    dut.unsigned_cmp = 1
    await Timer(1, units='ns')
    # Check output
    expected_val_1 = 0
    assert dut.breq.value == expected_val_1, (
        f"br_cmp={dut.breq.value}, expected={expected_val_1}"
    )
    expected_val_2 = 1
    assert dut.brlt.value == expected_val_2, (
        f"br_cmp={dut.brlt.value}, expected={expected_val_2}"
    )

@cocotb.test()
async def test_br_cmp_unsigned_2(dut):
    """Test Branch Comparator"""
    # Set inputs
    dut.rs1.value = 0b01111111111111111111111111111111
    dut.rs2.value = 0b01111111111111111111111111111111
    dut.unsigned_cmp = 1
    await Timer(1, units='ns')
    # Check output  
    expected_val_1 = 1
    assert dut.breq.value == expected_val_1, (
        f"br_cmp={dut.breq.value}, expected={expected_val_1}"
    )
    expected_val_2 = 0
    assert dut.brlt.value == expected_val_2, (
        f"br_cmp={dut.brlt.value}, expected={expected_val_2}"
    )
