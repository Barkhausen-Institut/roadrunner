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
    forever begin
        #10 clk = ~clk;
    end
end


endmodule