`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    01:26:37 06/19/2020 
// Design Name: 
// Module Name:    Data_Memory 
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
module Data_Memory(
    input CLK,
    input RST,
    input State_Memory,
    input [4:0] Address,
    input [7:0] Write_Data,
    input MemRead,
    input MemWrite,
    output reg [7:0] Read_Data
    );
	
	reg [7:0] mem[31:0];
	
	initial begin
		mem[0] <= 0;
		mem[1] <= 1;
		mem[2] <= 2;
		mem[3] <= 3;
		mem[4] <= 4;
		mem[5] <= 5;
		mem[6] <= 6;
		mem[7] <= 7;
		mem[8] <= 8;
		mem[9] <= 9;
		mem[10] <= 10;
		mem[11] <= 11;
		mem[12] <= 12;
		mem[13] <= 13;
		mem[14] <= 14;
		mem[15] <= 15;
		mem[16] <= 0;
		mem[17] <= -1;
		mem[18] <= -2;
		mem[19] <= -3;
		mem[20] <= -4;
		mem[21] <= -5;
		mem[22] <= -6;
		mem[23] <= -7;
		mem[24] <= -8;
		mem[25] <= -9;
		mem[26] <= -10;
		mem[27] <= -11;
		mem[28] <= -12;
		mem[29] <= -13;
		mem[30] <= -14;
		mem[31] <= -15;
	end
	
	always @(posedge RST or posedge State_Memory) begin
		if(RST) begin
			mem[0] <= 0;
			mem[1] <= 1;
			mem[2] <= 2;
			mem[3] <= 3;
			mem[4] <= 4;
			mem[5] <= 5;
			mem[6] <= 6;
			mem[7] <= 7;
			mem[8] <= 8;
			mem[9] <= 9;
			mem[10] <= 10;
			mem[11] <= 11;
			mem[12] <= 12;
			mem[13] <= 13;
			mem[14] <= 14;
			mem[15] <= 15;
			mem[16] <= 0;
			mem[17] <= -1;
			mem[18] <= -2;
			mem[19] <= -3;
			mem[20] <= -4;
			mem[21] <= -5;
			mem[22] <= -6;
			mem[23] <= -7;
			mem[24] <= -8;
			mem[25] <= -9;
			mem[26] <= -10;
			mem[27] <= -11;
			mem[28] <= -12;
			mem[29] <= -13;
			mem[30] <= -14;
			mem[31] <= -15;
		end else begin
			if(MemWrite == 1'b1) begin
				mem[Address] <= Write_Data;
			end
			if(MemRead == 1'b1) begin
				Read_Data <= mem[Address];
			end
		end
	end

endmodule
