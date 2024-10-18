`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    00:47:43 06/19/2020 
// Design Name: 
// Module Name:    PC 
// Project Name: 
// Target Devices: 
// Tool versions: 
// Description: 
//
// Dependencies: 
//
// Revision: 
// Revision 0.01 - File Created
// Additional Comments: 
//
//////////////////////////////////////////////////////////////////////////////////
module PC(
    input CLK,
    input RST,
    input [7:0] NewPC,
    output reg [7:0] PCout
    );
	
	reg ready;
	
	initial begin
		PCout <= 0;
		ready <= 0;
	end
	
	always @(posedge CLK or posedge RST) begin
		if(RST) begin
			PCout <= 0;
			ready <= 0;
		end else begin
			if(ready == 1'b0) begin
				ready <= 1;
			end else begin
				PCout <= NewPC;
			end
		end
	end

endmodule
