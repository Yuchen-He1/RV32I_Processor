# cocotb test for regfile
import cocotb
from cocotb.triggers import RisingEdge
from cocotb.triggers import Timer
from cocotb.clock import Clock

@cocotb.test()
async def x0_test(dut):
    """Test x0 register"""
    clock = Clock(dut.clk, 10, units='ns')
    cocotb.start_soon(clock.start())
    dut.rd_addr.value = 0
    dut.rd_data.value = 10
    dut.reg_write.value = 1
    await RisingEdge(dut.clk)
    dut.rs1_addr.value = 0
    await RisingEdge(dut.clk)
    expected_val = 0
    assert dut.rs1_data.value == expected_val, (
        f"registers[0]={dut.rs1_data.value}, expected={expected_val}"
    )

@cocotb.test()
async def regular_reg_test(dut):
    """Test regular register"""
    clock = Clock(dut.clk, 10, units='ns')
    cocotb.start_soon(clock.start())
    dut.rd_addr.value = 1
    dut.rd_data.value = 10
    dut.reg_write.value = 1
    await RisingEdge(dut.clk)
    dut.rs1_addr.value = 1
    await RisingEdge(dut.clk)
    expected_val = 10
    assert dut.rs1_data.value == expected_val, (
        f"registers[1]={dut.rs1_data.value}, expected={expected_val}"
    )
    
    dut.rs1_addr.value = 1
    await RisingEdge(dut.clk)
    assert dut.rs1_data.value == expected_val, (
        f"rs1_data={dut.rs1_data.value}, expected={expected_val}"
    )
    dut.rs2_addr.value = 1
    await RisingEdge(dut.clk)
    assert dut.rs2_data.value == expected_val, (
        f"rs2_data={dut.rs2_data.value}, expected={expected_val}"
    )
@cocotb.test()
async def reg_write_test(dut):
    """Test register write"""
    clock = Clock(dut.clk, 10, units='ns')
    cocotb.start_soon(clock.start())
    dut.rd_addr.value = 2
    dut.rd_data.value = 20
    dut.reg_write.value = 1
    await RisingEdge(dut.clk)

    dut.rs1_addr.value = 2
    await RisingEdge(dut.clk)
    expected_val = 20
    assert dut.rs1_data.value == expected_val, (
        f"registers[2]={dut.rs1_data.value}, expected={expected_val}"
    )

    dut.reg_write.value = 0
    dut.rd_addr.value = 2
    dut.rd_data.value = 10
    await RisingEdge(dut.clk)
    dut.rs1_addr.value = 2
    await RisingEdge(dut.clk)
    expected_val = 20
    assert dut.rs1_data.value == expected_val, (
        f"registers[2]={dut.rs1_data.value}, expected={expected_val}"
    )
