`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    01:17:35 06/19/2020 
// Design Name: 
// Module Name:    v7-Segment 
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
module v7_Segment(
    input [3:0] hex,
    output reg [6:0] seg
    );

	always begin
		case(hex)
			4'b0000 : seg <= 7'b0111111;
			4'b0001 : seg <= 7'b0000110;
			4'b0010 : seg <= 7'b1011011;
			4'b0011 : seg <= 7'b1001111;
			4'b0100 : seg <= 7'b1100110;
			4'b0101 : seg <= 7'b1101101;
			4'b0110 : seg <= 7'b1111101;
			4'b0111 : seg <= 7'b0000111;
			4'b1000 : seg <= 7'b1111111;
			4'b1001 : seg <= 7'b1101111;
			4'b1010 : seg <= 7'b1110111;
			4'b1011 : seg <= 7'b1111100;
			4'b1100 : seg <= 7'b0111001;
			4'b1101 : seg <= 7'b1011110;
			4'b1110 : seg <= 7'b1111001;
			4'b1111 : seg <= 7'b1110001;
		endcase
	end

endmodule
