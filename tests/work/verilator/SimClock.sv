`default_nettype none
module SimClock (
    output  wire logic  clk_o
);
    logic clk;

    export "DPI-C" task SetClock;
    import "DPI-C" context function void RegisterClock();

    initial RegisterClock();

    task SetClock;
        input bit val;
        clk = val;
    endtask

    assign clk_o = clk;

endmodule