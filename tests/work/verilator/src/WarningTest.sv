module WarningTest;

logic clk;
logic out;

initial begin
    clk = 1;
    forever #5 clk = ~clk;
end

logic shift[3];
assign out = shift[2];
assign shift[2] = shift[1];
assign shift[1] = shift[0];
assign shift[0] = clk;


endmodule