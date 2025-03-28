// this file is for pc adder constantly add 4 to pc

module Pc_adder (
    input wire [`DATA_WIDTH-1:0] i_pc,
    output wire [`DATA_WIDTH-1:0] o_pc_next
);
    assign o_pc_next = i_pc + 32'd4;
endmodule