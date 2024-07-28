`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    00:40:50 06/19/2020 
// Design Name: 
// Module Name:    Control 
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
module Control(
    input [1:0] Opcode,
    output [7:0] CtrlSign
    );

	//////////////////////////////
	//	CtrlSign Info			//
	//	index	|	Meaning		//
	//	7		|	RegDst		//
	//	6		|	RegWrite	//
	//	5		|	ALUSrc		//
	//	4		|	Branch		//
	//	3		|	MemRead		//
	//	2		|	MemWrite	//
	//	1		|	MemtoReg	//
	//	0		|	ALUOP		//
	//////////////////////////////
	
	assign CtrlSign = (Opcode == 2'b00) ? 8'b11000001 :
					(Opcode == 2'b01) ? 8'b01101010 :
					(Opcode == 2'b10) ? 8'b00100100 :
					8'b00010000;

endmodule
