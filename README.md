![](../../workflows/gds/badge.svg) ![](../../workflows/docs/badge.svg) ![](../../workflows/test/badge.svg) 
# The SSMCl proejct

This project contains two unsigned multipliers that have been developed using [Clash](http://www.clash-lang.org) and will be submitted to [TinyTapeout](https://tinytapeout.com/) shuttle number 10:

* A 3-bit version expecting two inputs in binary representation and a start signal and 
* a 8-bit version that exposes a streaming interface consisting of two input bits, one for each operand, and one start signal

They are designed with minimality in mind at the expence of required cycles. For fun, the designs have been developed using the Clash language.

### The general n-bit multiplier

The multiplier has three 1-bit inputs: a `start` signal and one signal for each input `x` and `y`. When `start` is asserted, the current values at `x` and `y` are taken as the least significant bit of the operands of the multiplication. The next $n-1$ cycles, the next bits of the operands should be made available at `x` and `y`. 

When the operands are fully streamed, the multiplier begins its operation for $n\cdot n$ cycles. After the computation is finished, the $2\cdot n$ bits of the product are streamed back; least significant bit first.

At the $(3+n)\cdot n$'th cycle, the full product is stremed back.

Asserting `start` before the multiplication has been fully carried out does not have any effect on the circuit, i.e. it is uninterruptible.


### 3-bit Multiplier
The 3-bit multiplier exposes a human friendly interface by accepting integer values as input, i.e. it wraps the general multiplier as described above. When `start` is asserted, the values at the `x` and `y` inputs are then being streamed into the actual multiplier, taking 3 cycles in total. The multiplier computes the product in 9 cycles and then steams back the 6-bit product in 6 cycles. The result can be seen at the output bit in cycle $18$. The result will remain valid until the next multiplication is started.The wave trace below illustrates this.

![wave trace for the 3-bit multiplier](docs/int3.png)



### 8-bit Multiplier
The 8-bit multiplier is simply a specialization of the general n-bit multiplier as explained above. The use it, use the bidiretional ports as described in the table in the pinout section below.

The following wave trace shows the multiplication 
$138 \cdot 86 =  (10101010)_2  \cdot (01010110)_2 = 11868 = (0010111001011100)_2$. 
To ease the reading, additional signals (`x'`, `y'`, `product'`) have been defined that show the low/high value as a number.

![wave trace for the 8-bit multiplier](docs/streaming8.png)