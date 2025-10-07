

module tb;

    logic clk;
    logic rst;
    logic [5:0] out;
    logic       outv;


    SimClock clk1 (
        .clk_o(clk)
    );
    
    SimClock clk2 (
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




endmodule
