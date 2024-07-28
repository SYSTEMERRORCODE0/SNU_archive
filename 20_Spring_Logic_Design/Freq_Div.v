`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    00:15:38 06/19/2020 
// Design Name: 
// Module Name:    Freq_Div 
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
module Freq_Div(
    input CLK_IN,
    input RST,
    output reg CLK,
    output reg [1:0] State
    );
	
	//50Mhz oscillator to 1hz Clock
	
	reg [31:0] cnt;
	
	initial begin
		State <= 2'b00;
	end
	
	always @(posedge CLK_IN) begin
		if(RST) begin
			cnt <= 32'd0;
			CLK <= 1'b0;
			State <= 2'b00;
		end else begin
			if(cnt == 32'd25000000) begin
				cnt <= 32'd0;
				if(CLK == 1'b0) begin
					State <= 2'b00;
				end
				CLK <= ~CLK;
			end else begin
				cnt <= cnt + 1;
				if(CLK == 1'b1) begin
					if(cnt == 32'd500) begin
						State <= 2'b01;
					end else if(cnt == 32'd1000) begin
						State <= 2'b10;
					end else if(cnt == 32'd1500) begin
						State <= 2'b11;
					end
				end
			end
		end
	end

endmodule
