#include <stdlib.h>
#include <iostream>
#include <verilated.h>
#include <verilated_vcd_c.h>
#include "Vtb.h"
#include "svdpi.h"
#include "Vtb__Dpi.h"

vluint64_t sim_time = 0;

using  std::cout, std::endl;

svScope scope;

void RegisterClock(){
    scope = svGetScope();
    const char *name = svGetNameFromScope(scope);
    cout << "register new clock @:" << name << endl;
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
        svSetScope(scope);
        SetClock(sim_time % 2);
    }

    m_trace->close();
    delete dut;
    exit(EXIT_SUCCESS);
}