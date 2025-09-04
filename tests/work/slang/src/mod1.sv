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

module mod1();

import RREnv::*;

initial begin
    `ifdef MOD1
        $display("GOOD mod1 defined as:%d", `MOD1);
    `else
        $display("BAAD mod1 NOT defined");
        RRFail;
        PanicModule pm;
    `endif    
    `ifdef MOD2
        $display("BAAD mod2 defined");
        RRFail;
        PanicModule pm2;
    `endif    
end 


endmodule