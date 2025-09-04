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

module mod2();

import RREnv::*;

initial begin
    `ifdef MOD2
        $display("GOOD mod2 defined");
    `else 
        $display("BAAD mod2 NOT defined");
        RRFail;
    `endif    
    `ifdef MOD1
        $display("BAAD mod1 defined");
        RRFail;
    `endif    
end 



endmodule