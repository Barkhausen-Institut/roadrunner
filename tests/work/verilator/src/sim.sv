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

logic clk;
initial begin
    clk = 1'b0;
    repeat(100) begin
        #10 clk = ~clk;
    end
end

initial RRSuccess();

endmodule