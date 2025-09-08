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

initial begin
    int num, num2;
    string msg, msg2;
    num = 14;
    msg = "hallo welt";
    $VPIArgs(msg, num, msg2, num2);
    $display("num:%d", num);
    $display("msg:%s", msg);
    $display("num2:%d", num2);
    $display("msg2:%s", msg2);
end


endmodule