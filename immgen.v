// this file is immediate number generator for single cycle processor.
// ISA based on RV32I
// it accepts 32-bit instruction and generates 32-bit immediate value.
// and have 2 select bits to select the type of immediate value to be generated.
module immgen (
    input [31:0] instruction,
    input [2:0] imm_select,
    output reg [31:0] imm
);



// imm_select = 000 -> I-type immediate
// imm_select = 001 -> S-type immediate
// imm_select = 010 -> B-type immediate
// imm_select = 011 -> J-type immediate
// imm_select = 100 -> U-type immediate

// I-type immediate = instruction[31:20]
// S-type immediate = {instruction[31:25], instruction[11:7]}
// B-type immediate = {instruction[31], instruction[7], instruction[30:25], instruction[11:8], 1'b0}
// J-type immediate = {instruction[31], instruction[19:12], instruction[20], instruction[30:21], 1'b0}  // 20 bits
// U-type immediate = instruction[31:12] << 12

always @* begin
    case (imm_select)
        3'b000: imm = {{20{instruction[31]}}, instruction[31:20]}; // I-type immediate
        3'b001: imm = {{20{instruction[31]}}, instruction[31:25], instruction[11:7]}; // S-type immediate
        3'b010: imm = {{19{instruction[31]}}, instruction[31], instruction[7], instruction[30:25], instruction[11:8], 1'b0}; // B-type immediate
        3'b011: imm = {{11{instruction[31]}}, instruction[31], instruction[19:12], instruction[20], instruction[30:21], 1'b0}; // J-type immediate
        3'b100: imm = {instruction[31:12], 12'b0}; // U-type immediate
        default: imm = 32'b0;
    endcase
end

endmodule