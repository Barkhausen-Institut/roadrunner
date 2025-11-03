

module tb;

    logic clk;
    logic rst;
    logic [5:0] out;
    logic       outv;


    SimClock #(
        .FREQUENCY(75 * SimHelper::MHZ)
    ) clk1 (
        .clk_o(clk)
    );
    
    SimClock #(
        .FREQUENCY(100 * SimHelper::MHZ)
    ) clk2 (
        .clk_o(rst)
    );
    
    alu alu(
        .clk    (clk),
        .rst    (rst),
        .op_in  (nop),
        .a_in   ('0),
        .b_in   ('0),
        .in_valid   ('0),
        .out    (out),
        .out_valid  (outv)
    );

    SimTime tme();

    initial begin
        $dumpfile("waveform.vcd");
        $dumpvars();
        tme.waitTime(1 * SimHelper::USEC);
        $finish();
    end




endmodule
