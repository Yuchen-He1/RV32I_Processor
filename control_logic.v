// this file is for control logic of RV32I 
// single cycle processor 
// it will generate control signals for ALU, MUX, and dMEM, brcmp

module control_logic (
    input wire [31:0] instruction,
    input wire breq,
    input wire brlt,
    output reg pcsel,
    output reg [3:0] alu_op,
    output reg operand1_sel,
    output reg operand2_sel,
    output reg reg_write,
    output reg [2:0] immgen_sel,
    output reg dmem_write,
    output reg dmem_read,
    output reg brunsigned,
    output reg [1:0] writeback_sel
);
    wire [6:0] opcode;
    wire [2:0] funct3;
    wire [6:0] funct7; 
    assign opcode = instruction[6:0];
    assign funct3 = instruction[14:12];
    assign funct7 = instruction[31:25];



    always @(*) begin
        case (opcode)
            7'b0110111: begin // LUI
            // pcsel = 1'b0;        // by deafult pc+4
            // // operdan1_sel = x0  should x0+imm
            // operand2_sel = 1'b0; // immeidate number
            // reg_write = 1'b1;    // write to rd
            // immgen_sel = 3'b100; // U-type immediate
            // dmem_read = 1'b0;    // no need to read from dmem
            // dmem_write = 1'b0;   // no need to write to dmem
            // brunsigned = 1'b0;   // no need to compare
            end
            7'b0010111: begin // AUIPC
            end
            7'b1101111: begin // JAL
            pcsel = 1'b1;        // not pc+4 instead address after alu computation
            operand1_sel = 1'b1; // current pc
            operand2_sel = 1'b0; // immeidate number 
            reg_write = 1'b1;    // write pc+4 to rd
            immgen_sel = 3'b011; // J-type immediate
            dmem_read = 1'b0;    // no need to read from dmem
            dmem_write = 1'b0;   // no need to write to dmem
            brunsigned = 1'b0;   // no need to compare
            writeback_sel = 2'b00; // write pc+4 to rd
            alu_op = 4'b0000;   // pc + imm use add operation
            end
            7'b1100111: begin // JALR
            pcsel = 1'b1;        // not pc+4 instead address after alu computation
            operand1_sel = 1'b0;  // rs1 
            operand2_sel = 1'b0; // immeidate number
            reg_write = 1'b1;    // write pc+4 to rd
            immgen_sel = 3'b000; // I-type immediate
            dmem_read = 1'b0;    // no need to read from dmem
            dmem_write = 1'b0;   // no need to write to dmem
            brunsigned = 1'b0;   // no need to compare
            writeback_sel = 2'b00; // write pc+4 to rd
            alu_op = 4'b0000;   // rs1 + imm use add operation
            end 
            7'b1100011: begin // B-type
                pcsel = 1'b0;    // by deafult pc+4
                immgen_sel = 3'b010; // B-type immediate    
                operand1_sel = 1'b1; // pc
                operand2_sel = 1'b0; // immeidate number
                reg_write = 1'b0;    // no need to write to rd
                dmem_read = 1'b0;    // no need to read from dmem
                dmem_write = 1'b0;   // no need to write to dmem
                brunsigned = 1'b0;   // by deafult signed compare
                writeback_sel = 2'b11; // no need to write to rd
                alu_op = 4'b0000;   // pc + imm use add operation
                case (funct3)
                    3'b000: begin // BEQ
                        if (breq) begin
                            pcsel = 1'b1;
                        end
                    end
                    3'b001: begin // BNE
                        if (~breq) begin
                            pcsel = 1'b1;
                        end
                    end
                    3'b100: begin // BLT
                        if (brlt) begin
                            pcsel = 1'b1;
                        end
                    end
                    3'b101: begin // BGE
                        if (~brlt) begin
                            pcsel = 1'b1;
                        end
                    end
                    3'b110: begin // BLTU
                        brunsigned = 1'b1;// unsigned compare
                        if (brlt) begin
                            pcsel = 1'b1;
                        end
                    end
                    3'b111: begin // BGEU
                        brunsigned = 1'b1;// unsigned compare
                        if (~brlt) begin
                            pcsel = 1'b1;
                        end
                    end
                endcase
            end
            //load & store only support lw,sw
            7'b0000011: begin // I-type load
                pcsel = 1'b0;    // by deafult pc+4
                operand1_sel = 1'b0; // rs1
                operand2_sel = 1'b0; // immeidate number
                reg_write = 1'b1;    // write to rd
                immgen_sel = 3'b000; // I-type immediate
                dmem_read = 1'b1;    // read from dmem
                dmem_write = 1'b0;   // no need to write to dmem
                brunsigned = 1'b0;   // no need to compare
                writeback_sel = 2'b01; // write data from dmem to rd
                alu_op = 4'b0000;   // rs1 + imm use add operation
            end
            7'b0100011: begin // S-type store
                pcsel = 1'b0;    // by deafult pc+4
                operand1_sel = 1'b0; // rs1
                operand2_sel = 1'b0; // immeidate number
                reg_write = 1'b0;    // no need to write to rd
                immgen_sel = 3'b001; // S-type immediate
                dmem_read = 1'b0;    // no need to read from dmem
                dmem_write = 1'b1;   // write to dmem
                brunsigned = 1'b0;   // no need to compare
                writeback_sel = 2'b11; // no need to write to rd
                alu_op = 4'b0000;   // rs1 + imm use add operation
            end
            7'b0010011: begin // I-type ALU
                pcsel = 1'b0;    // by deafult pc+4
                operand1_sel = 1'b0; // rs1
                operand2_sel = 1'b0; // immeidate number
                reg_write = 1'b1;    // write to rd
                immgen_sel = 3'b000; // I-type immediate
                dmem_read = 1'b0;    // no need to read from dmem
                dmem_write = 1'b0;   // no need to write to dmem
                brunsigned = 1'b0;   // no need to compare
                writeback_sel = 2'b10; // write data from ALU to rd
                case (funct3)
                    3'b000: begin // ADDI
                        alu_op = 4'b0000;
                    end
                    3'b010: begin // SLTI
                        alu_op = 4'b1001;
                    end
                    3'b011: begin // SLTIU
                        alu_op = 4'b1010;
                    end
                    3'b100: begin // XORI
                        alu_op = 4'b0100;
                    end
                    3'b110: begin // ORI
                        alu_op = 4'b0011;
                    end
                    3'b111: begin // ANDI
                        alu_op = 4'b0010;
                    end
                    3'b001: begin // SLLI
                        alu_op = 4'b0110;
                    end
                    3'b101: begin // SR?I
                    if (funct7[5]) begin
                        alu_op = 4'b1000; // SRAI
                    end else begin
                        alu_op = 4'b0111; // SRLI
                    end
                    end
                endcase
            end
            7'b0110011: begin // R-type ALU
                pcsel = 1'b0;    // by deafult pc+4
                operand1_sel = 1'b0; // rs1
                operand2_sel = 1'b1; // rs2
                reg_write = 1'b1;    // write to rd
                immgen_sel = 3'b111; //no need immediate number
                dmem_read = 1'b0;    // no need to read from dmem
                dmem_write = 1'b0;   // no need to write to dmem
                brunsigned = 1'b0;   // no need to compare
                writeback_sel = 2'b10; // write data from ALU to rd
                case (funct3)
                    3'b000: begin // ADD/SUB
                        if (funct7[5]) begin
                            alu_op = 4'b0001; // SUB
                        end else begin
                            alu_op = 4'b0000; // ADD
                        end
                    end
                    3'b001: begin // SLL
                        alu_op = 4'b0110;
                    end
                    3'b010: begin // SLT
                        alu_op = 4'b1001;
                    end
                    3'b011: begin // SLTU
                        alu_op = 4'b1010;
                        //brunsigned = 1'b1;
                    end
                    3'b100: begin // XOR
                        alu_op = 4'b0100;
                    end
                    3'b101: begin // SRL/SRA
                        if (funct7[5]) begin
                            alu_op = 4'b1000; // SRA
                        end else begin
                            alu_op = 4'b0111; // SRL
                        end
                    end
                    3'b110: begin // OR
                        alu_op = 4'b0011;
                    end
                    3'b111: begin // AND
                        alu_op = 4'b0010;
                    end
                endcase
            end
            default: begin
                // default values
                pcsel            = 1'b0;
                // operand1_sel 0-rs1 1-pc 
                operand1_sel     = 1'b0;
                // operand2_sel 0-imm 1-rs2
                operand2_sel     = 1'b0;
                reg_write        = 1'b0;
                immgen_sel       = 3'b000;
                dmem_write       = 1'b0;
                dmem_read        = 1'b0;
                brunsigned       = 1'b0;
                // writeback_sel 00-pc+4 01-dmem 10-alu 11-no writeback
                writeback_sel    = 2'b11;    
                alu_op           = 4'b0000; // default add operation
            end
            //deafult set no writeback and  no permission write reg

        endcase
    end
endmodule