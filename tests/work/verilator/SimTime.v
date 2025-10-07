`timescale 1ps/1ps
`default_nettype none

module SimTime;

function automatic signed[63:0] now;
    input reg i;
    now = $time;
endfunction

task waitTime(input signed[63:0] amount);
    #(amount);
endtask

endmodule
