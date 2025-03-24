// this file is Imem 
// Imem is a memory that stores the instructions
// It only supports read operation

module Imem (
    input wire [31:0] pc,
    output wire [31:0] instruction
);
    // initialize a constant memory(reg array) to store the instructions
    // use readmemh to read the instructions from the file
    reg [31:0] mem[0:1023];
    // for test purpose, we only have 64 instructions
    initial begin
        $readmemh("instructions.txt", mem);
        //$display("Mem[0] = %h", mem[0]);
    end

    
    assign instruction = mem[pc[31:2]];

    // each time pc change we will read the instruction from the memory
    // can ignore the last two bits of pc
    // since the instructions are 32 bits/4 bytes
    // we will only use the first 30 bits of pc to access the memory

    // debug info
    //     always @(pc) begin
    //     $display("PC = %h, Index = %h, Instruction = %h", pc, pc[31:2], mem[pc[31:2]]);
    // end
;  
    
endmodule