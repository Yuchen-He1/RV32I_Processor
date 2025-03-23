// this file is for ALU 
// ALU is a arithmetic logic unit
// it support add, sub, and, or, xor, nor,
//             sll, srl, sra, slt, sltu operation

module ALU (
    input wire [31:0] a,
    input wire [31:0] b,
    input wire [3:0] alu_control,
    output reg [31:0] result
);
    
    always @* begin
        case (alu_control)
            4'b0000: result = a + b; // add
            4'b0001: result = a - b; // sub
            4'b0010: result = a & b; // and
            4'b0011: result = a | b; // or
            4'b0100: result = a ^ b; // xor
            4'b0101: result = ~(a | b); // nor
            // 4'b0110: result = a << b; // sll
            // 4'b0111: result = a >> b; // srl
            // 4'b1000: result = $signed(a) >>> b; // sra
            4'b0110: result = a << b[4:0]; // sll
            4'b0111: result = a >> b[4:0]; // srl
            4'b1000: result = $signed(a) >>> b[4:0]; // sra

            // 4'b1001: result = (a < b) ? 32'b1 : 32'b0; // slt
            // 4'b1010: result = (a < b) ? 32'b1 : 32'b0; // sltu
            4'b1001: result = ($signed(a) < $signed(b)) ? 32'b1 : 32'b0; // slt (signed)
            4'b1010: result = (a < b) ? 32'b1 : 32'b0; // sltu (unsigned)
            default: result = 32'b0; // default case
        endcase
    end
    
endmodule