// this file is for pc adder constantly add 4 to pc
module pc_adder (
    input wire [31:0] pc,
    output wire [31:0] pc_next
);
    assign pc_next = pc + 32'd4;
endmodule