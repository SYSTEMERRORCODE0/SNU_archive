`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    00:58:03 06/19/2020 
// Design Name: 
// Module Name:    Registers 
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
module Registers(
    input CLK,
    input RST,
    input State_Reg_Write,
    input [1:0] Read_Reg1,
    input [1:0] Read_Reg2,
    input [1:0] Write_Reg,
    input [7:0] Reg_Write_Data,
    input RegWrite,
	input [1:0] Reg_Data_Select,
	output [7:0] Reg_Data,
    output [7:0] Read_Data1,
    output [7:0] Read_Data2,
    output reg [7:0] Reg_Write_Data_Save
    );

	reg [7:0] register[3:0];
	
	// Initialiize
	initial begin
		register[0] = 0;
		register[1] = 0;
		register[2] = 0;
		register[3] = 0;
	end
	
	assign Read_Data1 = (Read_Reg1 == 2'b00) ? register[0] :
						(Read_Reg1 == 2'b01) ? register[1] :
						(Read_Reg1 == 2'b10) ? register[2] :
						register[3];
						
	assign Read_Data2 = (Read_Reg2 == 2'b00) ? register[0] :
						(Read_Reg2 == 2'b01) ? register[1] :
						(Read_Reg2 == 2'b10) ? register[2] :
						register[3];
						
	assign Reg_Data = (Reg_Data_Select == 2'b00) ? register[0] :
					  (Reg_Data_Select == 2'b01) ? register[1] :
					  (Reg_Data_Select == 2'b10) ? register[2] :
					  (Reg_Data_Select == 2'b11) ? register[3] :
					  8'b00000000;
						
	always @(posedge RST or posedge State_Reg_Write) begin
		if(RST) begin
			register[0] = 0;
			register[1] = 0;
			register[2] = 0;
			register[3] = 0;
		end else begin
			Reg_Write_Data_Save = Reg_Write_Data;
			if(RegWrite == 1'b1) begin
				register[Write_Reg] = Reg_Write_Data;
			end
		end
	end

endmodule
