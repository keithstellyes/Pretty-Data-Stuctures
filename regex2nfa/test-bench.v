/*
 * This is a sample test bench template.
 * (notice the curly braces used for Python's .format()
 *
 * This is included in the out.v generated
 */
`define STDIN 32'h8000_0000
module main;
reg clk = 0;
reg [7:0] data;
wire [1:0] accept;
{} g(.clk(clk), .data(data), .accept(accept));

// Tests with P then Z
initial begin
    $display("WAIT: %b ACCEPT: %b REJECT: %b", `WAIT, `ACCEPT, `REJECT);
    $display("Regex: {}");
    while(!$feof(`STDIN)) begin
        #1 data = $fgetc(`STDIN);
	if(data != 8'hff) begin //EOF
	    #1 clk = 1;
	    #1 clk = 0;
	    $display("SENT:(%c) ACCEPT-STATE:(%b)", data, accept);
	end
    end
end
endmodule
