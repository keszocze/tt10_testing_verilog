# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

def myBin(val, minLen=3):
  valS = bin(val)[2:]

  while len(valS) < minLen:
    valS = "0" + valS

  return valS

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, units="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    await ClockCycles(dut.clk,1)

    assert dut.uo_out.value == 0

    for x in range(0,8):
        for y in range(0,8):
            print(f"Testing {x} * {y}")

            startMulInputS = "10" + myBin(x) + myBin(y)
            startMulInput = int(startMulInputS,2)

            endMulS = "10" + myBin(x*y,6)
            endMul = int(endMulS, 2)

            dut.ui_in.value = startMulInput

            for i in range(0,17):
                await ClockCycles(dut.clk,1)

                dut.ui_in.value = 0
                assert dut.uo_out.value == 0
                
            await ClockCycles(dut.clk,1)
            assert dut.uo_out.value == endMul

            # idle a couple of clock cyckles
            await ClockCycles(dut.clk,4)