`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    04:42:11 06/19/2020 
// Design Name: 
// Module Name:    ADD 
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
module ADD(
    input [7:0] NumA,
    input [7:0] NumB,
    output [7:0] Result
    );

	assign Result = NumA + NumB;

endmodule
