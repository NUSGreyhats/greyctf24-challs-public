module my_full_adder(input A, B, CIN, output S, COUT);
	assign S = A ^ B ^ CIN;
	assign COUT = (A & B) | (CIN & (A ^ B));
endmodule

module adder(input [31:0] A, input [31:0] B, input C0, output [31:0] S);
	wire C[32:0];
	
	my_full_adder fa0 (A[0], B[0], C0, S[0], C[1]);
	my_full_adder fa1 (A[1], B[1], C[1], S[1], C[2]);
    my_full_adder fa2 (A[2], B[2], C[2], S[2], C[3]);
    my_full_adder fa3 (A[3], B[3], C[3], S[3], C[4]);
    my_full_adder fa4 (A[4], B[4], C[4], S[4], C[5]);
    my_full_adder fa5 (A[5], B[5], C[5], S[5], C[6]);
    my_full_adder fa6 (A[6], B[6], C[6], S[6], C[7]);
    my_full_adder fa7 (A[7], B[7], C[7], S[7], C[8]);
    my_full_adder fa8 (A[8], B[8], C[8], S[8], C[9]);
    my_full_adder fa9 (A[9], B[9], C[9], S[9], C[10]);
    my_full_adder fa10 (A[10], B[10], C[10], S[10], C[11]);
    my_full_adder fa11 (A[11], B[11], C[11], S[11], C[12]);
    my_full_adder fa12 (A[12], B[12], C[12], S[12], C[13]);
    my_full_adder fa13 (A[13], B[13], C[13], S[13], C[14]);
    my_full_adder fa14 (A[14], B[14], C[14], S[14], C[15]);
    my_full_adder fa15 (A[15], B[15], C[15], S[15], C[16]);
    my_full_adder fa16 (A[16], B[16], C[16], S[16], C[17]);
    my_full_adder fa17 (A[17], B[17], C[17], S[17], C[18]);
    my_full_adder fa18 (A[18], B[18], C[18], S[18], C[19]);
    my_full_adder fa19 (A[19], B[19], C[19], S[19], C[20]);
    my_full_adder fa20 (A[20], B[20], C[20], S[20], C[21]);
    my_full_adder fa21 (A[21], B[21], C[21], S[21], C[22]);
    my_full_adder fa22 (A[22], B[22], C[22], S[22], C[23]);
    my_full_adder fa23 (A[23], B[23], C[23], S[23], C[24]);
    my_full_adder fa24 (A[24], B[24], C[24], S[24], C[25]);
    my_full_adder fa25 (A[25], B[25], C[25], S[25], C[26]);
    my_full_adder fa26 (A[26], B[26], C[26], S[26], C[27]);
    my_full_adder fa27 (A[27], B[27], C[27], S[27], C[28]);
    my_full_adder fa28 (A[28], B[28], C[28], S[28], C[29]);
    my_full_adder fa29 (A[29], B[29], C[29], S[29], C[30]);
    my_full_adder fa30 (A[30], B[30], C[30], S[30], C[31]);
    my_full_adder fa31 (A[31], B[31], C[31], S[31], C[32]);
endmodule

module counter(input clk, output reg [31:0] result);
    integer i;

    reg [31:0] temp;
    wire [31:0] out;
    adder a(temp, 1, 1'b0, out);

	initial begin
        result = 0;
        temp = 0;
        #1;
	end
    
    always @(posedge clk)
    begin
        result = out;
        temp = result;
    end
endmodule

//END
