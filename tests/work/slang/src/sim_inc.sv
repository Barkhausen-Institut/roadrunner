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

`include "values.svh"
`include "values2.svh"

initial $display(HELLO + " " + WORLD + "\n");

initial RRSuccess();

endmodule