#include <stdlib.h>
#include <iostream>
#include <verilated.h>
#include <verilated_vcd_c.h>
#include "Vtb.h"
#include "svdpi.h"
#include "Vtb__Dpi.h"

vluint64_t sim_time = 0;

using  std::cout, std::endl;

typedef struct {
    vluint64_t  cycle;
    vluint64_t  offset;
    svScope     scope;
} sim_clock_t;

std::vector<sim_clock_t> clocks;

vluint64_t e12 = 1000000000000ULL;

void RegisterClock(long long freq, long long offset) {
    svScope scope = svGetScope();
    const char *name = svGetNameFromScope(scope);
    vluint64_t cycle = e12 / freq;
    cout << "register new clock @:" << name << " cycle:" << cycle << " + " << offset << "ps" << endl;
    clocks.push_back({cycle, (vluint64_t)offset, scope});
}

int main(int argc, char** argv, char** env) {
    Vtb *dut = new Vtb;

    Verilated::traceEverOn(true);
    VerilatedVcdC *m_trace = new VerilatedVcdC;
    dut->trace(m_trace, 5);
    m_trace->open("waveform.vcd");


    while (!Verilated::gotFinish()) {
        dut->eval();
        m_trace->dump(sim_time);
        //cout << "Simulation time: " << sim_time << endl;
        sim_time += 1;
        for (auto &clk : clocks) {
            vluint64_t period = (sim_time - clk.offset) % clk.cycle;
            bool level = period < (clk.cycle / 2);
            svSetScope(clk.scope);
            SetClock(level);
        }
    }

    m_trace->close();
    delete dut;
    exit(EXIT_SUCCESS);
}