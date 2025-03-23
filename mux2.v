// this file is helper for 2 bit mux
module mux2 (
    input wire [31:0] a,
    input wire [31:0] b,
    input wire sel,
    output wire [31:0] out
);
    assign out = (sel) ? b : a;
endmodule