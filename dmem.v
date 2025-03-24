// this file is for dmem 
// dmem is a memory that store/load data
// it only support read/write operation

module Dmem (
    input wire clk,
    input wire rst,
    input wire store,
    input wire load,
    //input wire write_enable,
    input wire [31:0] addr,
    input wire [31:0] input_data,
    output reg [31:0] output_data
);
    reg [31:0] mem[0:1023];
    // init dmem all 0
    integer i;
    initial begin
        for (i = 0; i < 1024; i = i + 1) begin
            mem[i] = 32'b0;
        end
    end
    // sync write and sync read
    always @(posedge clk or posedge rst) begin
        if (rst) begin
            output_data <= 32'b0;
        end else begin
            if (store) 
                mem[addr[31:2]] <= input_data; 
                
            if (load) 
                output_data <= mem[addr[31:2]];
            else 
                output_data <= 32'b0;
        end
    end


endmodule