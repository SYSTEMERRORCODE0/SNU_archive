`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    04:41:09 06/19/2020 
// Design Name: 
// Module Name:    NewPC_Generator 
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
module NewPC_Generator(
    input [7:0] Read_Address,
    input Branch,
    input [7:0] Imm,
    output [7:0] NewPC
    );
	
	wire [7:0] Result_A1;
	wire [7:0] Result_A2;
	
	ADD A1(.NumA(Read_Address), .NumB(8'b00000001), .Result(Result_A1));	//Read_Address + 1
	ADD A2(.NumA(Result_Al), .NumB(Imm), .Result(Result_A2));				//Read_Address + 1 + Imm
	MUX M1(.NumA(Result_A1), .NumB(Result_A2), .Select(Branch), .Result(NewPC));	//Select between up two

endmodule
