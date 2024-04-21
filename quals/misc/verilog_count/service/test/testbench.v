module test();
    // Inputs
    reg clk;
    // Outputs
    wire [31:0] result;

    counter c(clk, result);

    initial begin
        clk = 0;
        $monitor("clk %b, result %d", clk, result);
        repeat(131076) begin
            #1 clk = ~clk;
        end
    end
endmodule