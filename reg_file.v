// this file is register file for single cycle processor.
// ISA based on RV32I

module reg_file (
    input wire clk,
    input wire rst,
    input [4:0] rs1_addr,
    input [4:0] rs2_addr,
    input [4:0] rd_addr,
    input [31:0] rd_data,
    input reg_write,
    output [31:0] rs1_data,
    output [31:0] rs2_data
);

    reg [31:0] registers [0:31];
    // x0 is hardwired to 0, if try to read x0 it will return 0
    assign rs1_data = (rs1_addr==5'b0) ? 32'b0 : registers[rs1_addr];
    assign rs2_data = (rs2_addr==5'b0) ? 32'b0 : registers[rs2_addr];

    always @(posedge clk) begin
        // reset remain empty
        // need to figure out when need reset
        if (reg_write && rd_addr != 5'b0) begin
            registers[rd_addr] <= rd_data;
        end
    end
endmodule
// this file is register file for single cycle processor.