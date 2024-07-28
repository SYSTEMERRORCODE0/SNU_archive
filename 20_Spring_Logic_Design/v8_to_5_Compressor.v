`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    01:29:14 06/19/2020 
// Design Name: 
// Module Name:    v8_to_5_Compressor 
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
module v8_to_5_Compressor(
    input [7:0] Address8bits,
    output [4:0] Address5bits
    );
	
	assign Address5bits = Address8bits[4:0];

endmodule
