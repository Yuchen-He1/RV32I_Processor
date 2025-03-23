// this file is for branch comparator 

// we support beq,bne,blt,bltu(bge,bgeu is implicit support
// since we support blt,bltu)
module brcmptop (
    input wire [31:0] rs1,
    input wire [31:0] rs2,
    input wire unsigned_cmp, //0 signed, 1 unsigned
    output wire breq, // 0 not equal, 1 equal
    output wire brlt  // 0 not less than, 1 less than
);
    wire temp_breq_s, temp_breq_u, temp_brlt_s, temp_brlt_u;
    brcmp cmp (
        .rs1(rs1),
        .rs2(rs2),
        .unsigned_cmp(unsigned_cmp),
        .breq_s(temp_breq_s),
        .breq_u(temp_breq_u),
        .brlt_s(temp_brlt_s),
        .brlt_u(temp_brlt_u)
    );
    helper_mux mux1 (
        .a(temp_breq_s),
        .b(temp_breq_u),
        .sel(unsigned_cmp),
        .out(breq)
    );
    helper_mux mux2 (
        .a(temp_brlt_s),
        .b(temp_brlt_u),
        .sel(unsigned_cmp),
        .out(brlt)
    );  
endmodule

module helper_mux (
    input wire a,
    input wire b,
    input wire sel,
    output wire out
);
    assign out = (sel) ? b : a;
endmodule

module brcmp (
    input wire [31:0] rs1,
    input wire [31:0] rs2,
    input wire unsigned_cmp, //0 signed, 1 unsigned
    // output wire breq, // 0 not equal, 1 equal
    // output wire brlt  // 0 not less than, 1 less than
    output wire breq_s, breq_u, brlt_s, brlt_u
);

    //beq signed
    assign breq_s = ($signed(rs1) == $signed(rs2)) ? 1 : 0;
    //beq unsigned
    assign breq_u = (rs1 == rs2) ? 1 : 0;
    //blt signed
    assign brlt_s = ($signed(rs1) < $signed(rs2)) ? 1 : 0;
    //blt unsigned
    assign brlt_u = (rs1 < rs2) ? 1 : 0;
endmodule

