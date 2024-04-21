
/* DONT SEND THIS - THIS WILL FAIL
module counter(input clk, output reg [31:0] result);
	initial begin
		result <= 0;
	end

    always @(posedge clk)
    begin
        result <= result + 1;
    end
endmodule
//END 
*/