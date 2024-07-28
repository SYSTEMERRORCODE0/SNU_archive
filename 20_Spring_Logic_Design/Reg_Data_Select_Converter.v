`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    05:44:38 06/19/2020 
// Design Name: 
// Module Name:    Reg_Data_Select_Converter 
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
module Reg_Data_Select_Converter(
    input [3:0] IN,
    output reg [1:0] OUT
    );
	
	always begin
		if(IN[0] == 1) begin
			OUT = 2'b00;
		end else if(IN[1] == 1) begin
			OUT = 2'b01;
		end else if(IN[2] == 1) begin
			OUT = 2'b10;
		end else if(IN[3] == 1) begin
			OUT = 2'b11;
		end
	end

endmodule
