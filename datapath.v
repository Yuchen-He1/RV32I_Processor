// this file is datapath for single cycle processor 
// Implements a RISC-V RV32I single cycle processor

module datapath (
    input wire clk,
    input wire rst
);
    // Program Counter and Next PC wires
    wire [31:0] pc_current;
    wire [31:0] pc_plus_4;
    wire [31:0] pc_target;
    wire [31:0] pc_next;
    wire pcsel;

    // Instruction and immediate generation
    wire [31:0] instruction;
    wire [31:0] imm;
    wire [2:0] immgen_sel;

    // Register file wires
    wire [31:0] rs1_data, rs2_data;
    wire [31:0] rd_data;
    wire reg_write;

    // Branch comparison wires
    wire breq, brlt;
    wire brunsigned;

    // ALU wires
    wire [31:0] alu_operand1, alu_operand2;
    wire [31:0] alu_result;
    wire [3:0] alu_op;
    wire operand1_sel, operand2_sel;

    // Data memory wires
    wire [31:0] dmem_read_data;
    wire dmem_write, dmem_read;
    wire [1:0] writeback_sel;

    // PC register
    reg [31:0] PC;
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            PC <= 32'h00000000;
        end else begin
            PC <= pc_next;
        end
    end
    assign pc_current = PC;

    // PC Adder - calculates PC+4
    pc_adder pc_adder_inst (
        .pc(pc_current),
        .pc_next(pc_plus_4)
    );

    // MUX for PC selection - choose between PC+4 or branch/jump target
    mux2 pc_mux (
        .a(pc_plus_4),      // PC+4 (default next instruction)
        .b(alu_result),     // Branch/jump target
        .sel(pcsel),        // PC selection from control unit
        .out(pc_next)       // Next PC value
    );

    // Instruction Memory
    Imem imem_inst (
        .pc(pc_current),
        .instruction(instruction)
    );

    // Control Logic
    control_logic control_logic_inst (
        .instruction(instruction),
        .breq(breq),
        .brlt(brlt),
        .pcsel(pcsel),
        .alu_op(alu_op),
        .operand1_sel(operand1_sel),
        .operand2_sel(operand2_sel),
        .reg_write(reg_write),
        .immgen_sel(immgen_sel),
        .dmem_write(dmem_write),
        .dmem_read(dmem_read),
        .brunsigned(brunsigned),
        .writeback_sel(writeback_sel)
    );

    // Immediate Generator
    immgen immgen_inst (
        .instruction(instruction),
        .imm_select(immgen_sel),
        .imm(imm)
    );

    // Register File
    reg_file reg_file_inst (
        .clk(clk),
        .rst(rst),
        .rs1_addr(instruction[19:15]),
        .rs2_addr(instruction[24:20]),
        .rd_addr(instruction[11:7]),
        .rd_data(rd_data),
        .reg_write(reg_write),
        .rs1_data(rs1_data),
        .rs2_data(rs2_data)
    );

    // Branch Comparator
    brcmptop branch_comparator (
        .rs1(rs1_data),
        .rs2(rs2_data),
        .unsigned_cmp(brunsigned),
        .breq(breq),
        .brlt(brlt)
    );

    // MUX for ALU operand 1 selection
    mux2 alu_operand1_mux (
        .a(rs1_data),       // rs1 value
        .b(pc_current),     // PC value (for branches/jumps)
        .sel(operand1_sel), // Selection signal
        .out(alu_operand1)  // Selected operand 1
    );

    // MUX for ALU operand 2 selection
    mux2 alu_operand2_mux (
        .a(imm),            // Immediate value
        .b(rs2_data),       // rs2 value
        .sel(operand2_sel), // Selection signal
        .out(alu_operand2)  // Selected operand 2
    );

    // ALU
    ALU alu_inst (
        .a(alu_operand1),
        .b(alu_operand2),
        .alu_control(alu_op),
        .result(alu_result)
    );

    // Data Memory
    Dmem dmem_inst (
        .clk(clk),
        .rst(rst),
        .store(dmem_write),
        .load(dmem_read),
        .addr(alu_result),
        .input_data(rs2_data),
        .output_data(dmem_read_data)
    );

    // Write-back MUX (4-input MUX for selecting what to write to the register file)
    mux4 writeback_mux (
        .a(pc_plus_4),      // PC+4 (for JAL/JALR)
        .b(dmem_read_data), // Memory load data
        .c(alu_result),     // ALU result
        .d(32'h00000000),   // Not used (could be used for CSR or other future extensions)
        .sel(writeback_sel),
        .out(rd_data)
    );

endmodule