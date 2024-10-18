`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date:    00:13:30 06/19/2020 
// Design Name: 
// Module Name:    Microprocessor 
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
module Microprocessor(
    input [7:0] Instruction,
    input CLK_IN,
    input RST,
	input [3:0] SEL_REG,
    output [7:0] Read_Address,	//same as PC
    output [6:0] SEG1,  // bigger digit
	output [6:0] SEG2,	// smaller digit
	output [6:0] SEG3,  // PC bigger digit
	output [6:0] SEG4,	// PC smaller digit
	output [6:0] SEG5,  // test bigger digit
	output [6:0] SEG6	// test smaller digit
    );
	
	//////////////////////////////////////////
	// Instruction Info						//
	//	index(Type)	|	Meaning				//
	//	7:6	(all)	|	Opcode(op)			//
	//	5:4	(R, I)	|	SourceReg1(rs)		//
	//	3:2 (R, I)	|	SourceReg2(rt)		//
	//	1:0	(R)		|	DestinationReg(rd)	//
	//	1:0 (I, J)	|	immediate(imm)		//
	//////////////////////////////////////////
	
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
	
	wire CLK;				// Just a Clock
	wire [1:0] State;		// For Control the timing
	wire [7:0] CtrlSign;	// Control Sign
	wire [7:0] Imm;			// Ummediate (constant)
	wire [7:0] Read_Data1;		// Result of Read register1
	wire [7:0] Read_Data2;		// Result of Read register2
	wire [7:0] ALU_Result;	// Result of ALU
	wire [7:0] Read_Data;	// Result of Data memory
	wire [7:0] Reg_Write_Data_Save;	// What to must show 
	wire State_Reg_Write;	// Write on register when this is 1
	wire State_Memory;		// activate memory r/w when this is 1
	wire [7:0] NewPC;
	wire [1:0] Write_Reg;
	wire [7:0] Reg_Write_Data;	//
	wire [7:0] ALU_Input2;
	wire [4:0] ALU_Result_5;		// Compressed ALU_Result
	wire [1:0] Reg_Data_Select;		//what reg to watch
	wire [7:0] Reg_Data;
	
	//CLK generator
	Freq_Div FD1(.CLK_IN(CLK_IN), .RST(RST), .CLK(CLK), .State(State));	//Get 1hz CLK
	
	//State Control
	State_Control SC1(.State(State), .State_Reg_Write(State_Reg_Write), .State_Memory(State_Memory));	//transform State into Specific Control
	
	//Control Unit
	Control C1(.Opcode(Instruction[7:6]), .CtrlSign(CtrlSign));	//Send CtrlUnit Opcode
	
	//NewPC Generator
	//NewPC_Generator NPG1(.Read_Address(Read_Address), .Branch(CtrlSign[4]), .Imm(Imm), .NewPC(NewPC));
	
	//PC
	PC P1(.CLK(CLK), .RST(RST), .NewPC(CtrlSign[4] ? (Read_Address + 8'b00000001 + Imm) : (Read_Address + 8'b00000001)), .PCout(Read_Address));
	
	assign Write_Reg = (CtrlSign[7] == 1) ? Instruction[1:0] : Instruction[3:2];
	
	MUX M2(.NumA(ALU_Result), .NumB(Read_Data), .Select(CtrlSign[1]), .Result(Reg_Write_Data));
	
	//Reg_Data_Select GEN
	Reg_Data_Select_Converter RDSC1(.IN(SEL_REG), .OUT(Reg_Data_Select));
	
	//Registers
	Registers R1(.CLK(CLK), .RST(RST), .State_Reg_Write(State_Reg_Write), .Read_Reg1(Instruction[5:4]), 
				.Read_Reg2(Instruction[3:2]), .Write_Reg(Write_Reg), .Reg_Write_Data(Reg_Write_Data), 
				.RegWrite(CtrlSign[6]), .Read_Data1(Read_Data1), .Read_Data2(Read_Data2), 
				.Reg_Write_Data_Save(Reg_Write_Data_Save), .Reg_Data_Select(Reg_Data_Select),
				.Reg_Data(Reg_Data));
		
	//Make ALU_Input2
	MUX M3(.NumA(Read_Data2), .NumB(Imm), .Select(CtrlSign[5]), .Result(ALU_Input2));
	
	//ALU
	ALU A1(.NumA(Read_Data1), .NumB(ALU_Input2), .ALUOP(CtrlSign[0]), .Result(ALU_Result));
	
	//Data Memory Address 8bits to 5bits
	v8_to_5_Compressor COMP1(.Address8bits(ALU_Result), .Address5bits(ALU_Result_5));
	
	//Data Memory
	Data_Memory D1(.CLK(CLK), .RST(RST), .State_Memory(State_Memory), .Address(ALU_Result_5),
				.Write_Data(Read_Data2), .MemRead(CtrlSign[3]), .MemWrite(CtrlSign[2]), .Read_Data(Read_Data));
				
	//Sign Extension
	Sign_Extend SE1(.IN(Instruction[1:0]), .OUT(Imm));
	
	v7_Segment V1(.hex(Reg_Write_Data_Save[7:4]), .seg(SEG1));
	v7_Segment V2(.hex(Reg_Write_Data_Save[3:0]), .seg(SEG2));
	v7_Segment V3(.hex(Read_Address[7:4]), .seg(SEG3));
	v7_Segment V4(.hex(Read_Address[3:0]), .seg(SEG4));
	v7_Segment V5(.hex(Reg_Data[7:4]), .seg(SEG5));
	v7_Segment V6(.hex(Reg_Data[3:0]), .seg(SEG6));

endmodule
