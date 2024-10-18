; Write your own check here.
; Feel free to add arguments to @f, so its signature becomes @f(i32 %x, ...).
; But, this file should contain one function @f() only.
; FileCheck syntax: https://llvm.org/docs/CommandGuide/FileCheck.html

; This testcase if for checking the continuous optimization a little bit different
; And also infinite loop in switching same operand to operand that I trapped.
; in line 195, %cond4 = icmp eq i32 %a, %e trapped me %e -> %e infinite loop.

define i32 @f(i32 %e, i32 %c, i32 %d, i32 %a, i32 %b, i32 %f) {
; CHECK-LABEL: define i32 @f(i32 %e, i32 %c, i32 %d, i32 %a, i32 %b, i32 %f)
; CHECK-NEXT:    [[COND:%.*]] = icmp eq i32 [[A:%.*]], [[B:%.*]]
; CHECK-NEXT:    br i1 [[COND]], label [[BB_TRUE:%.*]], label [[BB_FALSE:%.*]]
; CHECK:       bb_true:
; CHECK-NEXT:    [[V1:%.*]] = add i32 [[A]], [[A]]
; CHECK-NEXT:    [[V2:%.*]] = add i32 [[A]], [[C:%.*]]
; CHECK-NEXT:    [[V3:%.*]] = add i32 [[A]], [[D:%.*]]
; CHECK-NEXT:    [[V4:%.*]] = add i32 [[A]], [[E:%.*]]
; CHECK-NEXT:    [[V5:%.*]] = add i32 [[A]], [[F:%.*]]
; CHECK-NEXT:    [[V6:%.*]] = add i32 [[A]], [[C]]
; CHECK-NEXT:    [[V7:%.*]] = add i32 [[A]], [[D]]
; CHECK-NEXT:    [[V8:%.*]] = add i32 [[A]], [[E]]
; CHECK-NEXT:    [[V9:%.*]] = add i32 [[A]], [[F]]
; CHECK-NEXT:    [[V10:%.*]] = add i32 [[C]], [[D]]
; CHECK-NEXT:    [[V11:%.*]] = add i32 [[C]], [[E]]
; CHECK-NEXT:    [[V12:%.*]] = add i32 [[C]], [[F]]
; CHECK-NEXT:    [[V13:%.*]] = add i32 [[D]], [[E]]
; CHECK-NEXT:    [[V14:%.*]] = add i32 [[D]], [[F]]
; CHECK-NEXT:    [[V15:%.*]] = add i32 [[E]], [[F]]
; CHECK-NEXT:    [[COND1:%.*]] = icmp eq i32 [[C]], [[A]]
; CHECK-NEXT:    br i1 [[COND1]], label [[BB_TRUE2:%.*]], label [[BB_FALSE:%.*]]
; CHECK:       bb_true2:
; CHECK-NEXT:    [[W1:%.*]] = add i32 [[C]], [[C]]
; CHECK-NEXT:    [[W2:%.*]] = add i32 [[C]], [[C]]
; CHECK-NEXT:    [[W3:%.*]] = add i32 [[C]], [[D]]
; CHECK-NEXT:    [[W4:%.*]] = add i32 [[C]], [[E]]
; CHECK-NEXT:    [[W5:%.*]] = add i32 [[C]], [[F]]
; CHECK-NEXT:    [[W6:%.*]] = add i32 [[C]], [[C]]
; CHECK-NEXT:    [[W7:%.*]] = add i32 [[C]], [[D]]
; CHECK-NEXT:    [[W8:%.*]] = add i32 [[C]], [[E]]
; CHECK-NEXT:    [[W9:%.*]] = add i32 [[C]], [[F]]
; CHECK-NEXT:    [[W10:%.*]] = add i32 [[C]], [[D]]
; CHECK-NEXT:    [[W11:%.*]] = add i32 [[C]], [[E]]
; CHECK-NEXT:    [[W12:%.*]] = add i32 [[C]], [[F]]
; CHECK-NEXT:    [[W13:%.*]] = add i32 [[D]], [[E]]
; CHECK-NEXT:    [[W14:%.*]] = add i32 [[D]], [[F]]
; CHECK-NEXT:    [[W15:%.*]] = add i32 [[E]], [[F]]
; CHECK-NEXT:    [[COND2:%.*]] = icmp eq i32 [[D]], [[C]]
; CHECK-NEXT:    br i1 [[COND2]], label [[BB_TRUE3:%.*]], label [[BB_FALSE:%.*]]
; CHECK:       bb_true3:
; CHECK-NEXT:    [[X1:%.*]] = add i32 [[C]], [[C]]
; CHECK-NEXT:    [[X2:%.*]] = add i32 [[C]], [[C]]
; CHECK-NEXT:    [[X3:%.*]] = add i32 [[C]], [[C]]
; CHECK-NEXT:    [[X4:%.*]] = add i32 [[C]], [[E]]
; CHECK-NEXT:    [[X5:%.*]] = add i32 [[C]], [[F]]
; CHECK-NEXT:    [[X6:%.*]] = add i32 [[C]], [[C]]
; CHECK-NEXT:    [[X7:%.*]] = add i32 [[C]], [[C]]
; CHECK-NEXT:    [[X8:%.*]] = add i32 [[C]], [[E]]
; CHECK-NEXT:    [[X9:%.*]] = add i32 [[C]], [[F]]
; CHECK-NEXT:    [[X10:%.*]] = add i32 [[C]], [[C]]
; CHECK-NEXT:    [[X11:%.*]] = add i32 [[C]], [[E]]
; CHECK-NEXT:    [[X12:%.*]] = add i32 [[C]], [[F]]
; CHECK-NEXT:    [[X13:%.*]] = add i32 [[C]], [[E]]
; CHECK-NEXT:    [[X14:%.*]] = add i32 [[C]], [[F]]
; CHECK-NEXT:    [[X15:%.*]] = add i32 [[E]], [[F]]
; CHECK-NEXT:    [[COND3:%.*]] = icmp eq i32 [[C]], [[E]]
; CHECK-NEXT:    br i1 [[COND3]], label [[BB_TRUE4:%.*]], label [[BB_FALSE:%.*]]
; CHECK:       bb_true4:
; CHECK-NEXT:    [[Y1:%.*]] = add i32 [[E]], [[E]]
; CHECK-NEXT:    [[Y2:%.*]] = add i32 [[E]], [[E]]
; CHECK-NEXT:    [[Y3:%.*]] = add i32 [[E]], [[E]]
; CHECK-NEXT:    [[Y4:%.*]] = add i32 [[E]], [[E]]
; CHECK-NEXT:    [[Y5:%.*]] = add i32 [[E]], [[F]]
; CHECK-NEXT:    [[Y6:%.*]] = add i32 [[E]], [[E]]
; CHECK-NEXT:    [[Y7:%.*]] = add i32 [[E]], [[E]]
; CHECK-NEXT:    [[Y8:%.*]] = add i32 [[E]], [[E]]
; CHECK-NEXT:    [[Y9:%.*]] = add i32 [[E]], [[F]]
; CHECK-NEXT:    [[Y10:%.*]] = add i32 [[E]], [[E]]
; CHECK-NEXT:    [[Y11:%.*]] = add i32 [[E]], [[E]]
; CHECK-NEXT:    [[Y12:%.*]] = add i32 [[E]], [[F]]
; CHECK-NEXT:    [[Y13:%.*]] = add i32 [[E]], [[E]]
; CHECK-NEXT:    [[Y14:%.*]] = add i32 [[E]], [[F]]
; CHECK-NEXT:    [[Y15:%.*]] = add i32 [[E]], [[F]]
; CHECK-NEXT:    [[COND4:%.*]] = icmp eq i32 [[E]], [[E]]
; CHECK-NEXT:    br i1 [[COND4]], label [[BB_TRUE5:%.*]], label [[BB_FALSE:%.*]]
; CHECK:       bb_true5:
; CHECK-NEXT:    [[Z1:%.*]] = add i32 [[E]], [[E]]
; CHECK-NEXT:    [[Z2:%.*]] = add i32 [[E]], [[E]]
; CHECK-NEXT:    [[Z3:%.*]] = add i32 [[E]], [[E]]
; CHECK-NEXT:    [[Z4:%.*]] = add i32 [[E]], [[E]]
; CHECK-NEXT:    [[Z5:%.*]] = add i32 [[E]], [[F]]
; CHECK-NEXT:    [[Z6:%.*]] = add i32 [[E]], [[E]]
; CHECK-NEXT:    [[Z7:%.*]] = add i32 [[E]], [[E]]
; CHECK-NEXT:    [[Z8:%.*]] = add i32 [[E]], [[E]]
; CHECK-NEXT:    [[Z9:%.*]] = add i32 [[E]], [[F]]
; CHECK-NEXT:    [[Z10:%.*]] = add i32 [[E]], [[E]]
; CHECK-NEXT:    [[Z11:%.*]] = add i32 [[E]], [[E]]
; CHECK-NEXT:    [[Z12:%.*]] = add i32 [[E]], [[F]]
; CHECK-NEXT:    [[Z13:%.*]] = add i32 [[E]], [[E]]
; CHECK-NEXT:    [[Z14:%.*]] = add i32 [[E]], [[F]]
; CHECK-NEXT:    [[Z15:%.*]] = add i32 [[E]], [[F]]
; CHECK-NEXT:    br label [[BB_EXIT:%.*]]
; CHECK:       bb_false:
; CHECK-NEXT:    [[Z16:%.*]] = add i32 [[A]], [[B]]
; CHECK-NEXT:    [[Z17:%.*]] = add i32 [[A]], [[C]]
; CHECK-NEXT:    [[Z18:%.*]] = add i32 [[A]], [[D]]
; CHECK-NEXT:    [[Z19:%.*]] = add i32 [[A]], [[E]]
; CHECK-NEXT:    [[Z20:%.*]] = add i32 [[A]], [[F]]
; CHECK-NEXT:    [[Z21:%.*]] = add i32 [[B]], [[C]]
; CHECK-NEXT:    [[Z22:%.*]] = add i32 [[B]], [[D]]
; CHECK-NEXT:    [[Z23:%.*]] = add i32 [[B]], [[E]]
; CHECK-NEXT:    [[Z24:%.*]] = add i32 [[B]], [[F]]
; CHECK-NEXT:    [[Z25:%.*]] = add i32 [[C]], [[D]]
; CHECK-NEXT:    [[Z26:%.*]] = add i32 [[C]], [[E]]
; CHECK-NEXT:    [[Z27:%.*]] = add i32 [[C]], [[F]]
; CHECK-NEXT:    [[Z28:%.*]] = add i32 [[D]], [[E]]
; CHECK-NEXT:    [[Z29:%.*]] = add i32 [[D]], [[F]]
; CHECK-NEXT:    [[Z30:%.*]] = add i32 [[E]], [[F]]
; CHECK-NEXT:    br label [[BB_EXIT]]
; CHECK:       bb_exit:
; CHECK-NEXT:    ret i32 [[C]]
;
  %cond = icmp eq i32 %a, %b
  br i1 %cond, label %bb_true, label %bb_false
bb_true:
  %v1 = add i32 %a, %b
  %v2 = add i32 %a, %c
  %v3 = add i32 %a, %d
  %v4 = add i32 %a, %e
  %v5 = add i32 %a, %f
  %v6 = add i32 %b, %c
  %v7 = add i32 %b, %d
  %v8 = add i32 %b, %e
  %v9 = add i32 %b, %f
  %v10 = add i32 %c, %d
  %v11 = add i32 %c, %e
  %v12 = add i32 %c, %f
  %v13 = add i32 %d, %e
  %v14 = add i32 %d, %f
  %v15 = add i32 %e, %f
  %cond1 = icmp eq i32 %c, %a
  br i1 %cond1, label %bb_true2, label %bb_false
bb_true2:
  %w1 = add i32 %a, %b
  %w2 = add i32 %a, %c
  %w3 = add i32 %a, %d
  %w4 = add i32 %a, %e
  %w5 = add i32 %a, %f
  %w6 = add i32 %b, %c
  %w7 = add i32 %b, %d
  %w8 = add i32 %b, %e
  %w9 = add i32 %b, %f
  %w10 = add i32 %c, %d
  %w11 = add i32 %c, %e
  %w12 = add i32 %c, %f
  %w13 = add i32 %d, %e
  %w14 = add i32 %d, %f
  %w15 = add i32 %e, %f
  %cond2 = icmp eq i32 %d, %a
  br i1 %cond2, label %bb_true3, label %bb_false
bb_true3:
  %x1 = add i32 %a, %b
  %x2 = add i32 %a, %c
  %x3 = add i32 %a, %d
  %x4 = add i32 %a, %e
  %x5 = add i32 %a, %f
  %x6 = add i32 %b, %c
  %x7 = add i32 %b, %d
  %x8 = add i32 %b, %e
  %x9 = add i32 %b, %f
  %x10 = add i32 %c, %d
  %x11 = add i32 %c, %e
  %x12 = add i32 %c, %f
  %x13 = add i32 %d, %e
  %x14 = add i32 %d, %f
  %x15 = add i32 %e, %f
  %cond3 = icmp eq i32 %a, %e
  br i1 %cond3, label %bb_true4, label %bb_false
bb_true4:
  %y1 = add i32 %a, %b
  %y2 = add i32 %a, %c
  %y3 = add i32 %a, %d
  %y4 = add i32 %a, %e
  %y5 = add i32 %a, %f
  %y6 = add i32 %b, %c
  %y7 = add i32 %b, %d
  %y8 = add i32 %b, %e
  %y9 = add i32 %b, %f
  %y10 = add i32 %c, %d
  %y11 = add i32 %c, %e
  %y12 = add i32 %c, %f
  %y13 = add i32 %d, %e
  %y14 = add i32 %d, %f
  %y15 = add i32 %e, %f
  %cond4 = icmp eq i32 %a, %e
  br i1 %cond4, label %bb_true5, label %bb_false
bb_true5:
  %z1 = add i32 %a, %b
  %z2 = add i32 %a, %c
  %z3 = add i32 %a, %d
  %z4 = add i32 %a, %e
  %z5 = add i32 %a, %f
  %z6 = add i32 %b, %c
  %z7 = add i32 %b, %d
  %z8 = add i32 %b, %e
  %z9 = add i32 %b, %f
  %z10 = add i32 %c, %d
  %z11 = add i32 %c, %e
  %z12 = add i32 %c, %f
  %z13 = add i32 %d, %e
  %z14 = add i32 %d, %f
  %z15 = add i32 %e, %f
  br label %bb_exit
bb_false:
  %z16 = add i32 %a, %b
  %z17 = add i32 %a, %c
  %z18 = add i32 %a, %d
  %z19 = add i32 %a, %e
  %z20 = add i32 %a, %f
  %z21 = add i32 %b, %c
  %z22 = add i32 %b, %d
  %z23 = add i32 %b, %e
  %z24 = add i32 %b, %f
  %z25 = add i32 %c, %d
  %z26 = add i32 %c, %e
  %z27 = add i32 %c, %f
  %z28 = add i32 %d, %e
  %z29 = add i32 %d, %f
  %z30 = add i32 %e, %f
  br label %bb_exit
bb_exit:
  ret i32 %c
}