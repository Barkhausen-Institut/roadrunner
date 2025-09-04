////    ////////////
////    ////////////
////
////
////////////    ////
////////////    ////
////    ////    ////
////    ////    ////
////////////
////////////

module SimTest();

import RREnv::*;

initial $display("Hallo Welt!\n");

typedef struct packed {
    logic       a;
    logic [7:0] b;
} sample_t;

logic       clk;
sample_t    sample;
initial begin
    clk = 1'b0;
    sample = '{a: 0, b: 'd3};
    repeat(100) begin
        #10 clk = ~clk;
        sample.b = sample.b + 1;
    end
end

initial begin
    #1000 $finish();
end

initial RRSuccess();

endmodule