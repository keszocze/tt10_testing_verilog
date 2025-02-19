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

    #for x in range(0,8):
    #    for y in range(0,8):
    #        dut._log.info(f"Testing {x} * {y} (3 bit, Int)")

            #startMulInputS = "10" + myBin(x) + myBin(y)
            #startMulInput = int(startMulInputS,2)

            #endMulS = "10" + myBin(x*y,6)
            #endMul = int(endMulS, 2)

            #dut.ui_in.value = startMulInput

            #await ClockCycles(dut.clk, 1)
            #dut.ui_in.value = 0
            
            #await ClockCycles(dut.clk,17)
                
            #assert dut.uo_out.value == endMul

            # idle a couple of clock cykles
            #await ClockCycles(dut.clk,4)

    for x in range(5,21):
        for y in range(2,3):
            xS = myBin(x,8)
            yS = myBin(y,8)
            pS = myBin(x*y,16)
            dut._log.info(f"Testing {x}({xS}) * {y}({yS}) = {x*y}({pS})(8 bit, Streaming)")
            for i in range (0,8):
                dut._log.info(f"Setting to {int("000001" + xS[7-i] + yS[7-i],2)}")
                dut.uio_in.value = int("000001" + xS[7-i] + yS[7-i],2)
                await ClockCycles(dut.clk,1)
            
            dut.uio_in.value = 0
            await ClockCycles(dut.clk,64)
            
            
            for i in range(0,16):
                outS = myBin(dut.uio_out.value,8)
                assert outS[7] == '1'
                assert outS[6] == pS[15-i]
                await ClockCycles(dut.clk,1)

            # wait to see something in the wave trace, no real test here right now
            