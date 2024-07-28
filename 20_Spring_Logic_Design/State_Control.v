`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    02:18:52 06/19/2020 
// Design Name: 
// Module Name:    State_Control 
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
module State_Control(
    input [1:0] State,
    output State_Reg_Write,
    output State_Memory
    );
	
	assign State_Reg_Write = State[1];
	assign State_Memory = State[0];

endmodule
