; Write your own check here.
; Feel free to add arguments to @f, so its signature becomes @f(i32 %x, ...).
; But, this file should contain one function @f() only.
; FileCheck syntax: https://llvm.org/docs/CommandGuide/FileCheck.html

; This testcase is for checking domination.
; There is no domination from entry to bb_exit, so there will be NO optimization
; There will be domination from bb_entry2 to bb_exit2, so %b -> %a in bb_true2

define i32 @f(i32 %x, i32 %y) {
; CHECK-LABEL: define i32 @f(i32 %x, i32 %y)
; CHECK-NEXT:    [[COND:%.*]] = icmp eq i32 [[X:%.*]], [[Y:%.*]]
; CHECK-NEXT:    br i1 [[COND]], label [[BB_TRUE:%.*]], label [[BB_FALSE:%.*]]
; CHECK:       bb_true:
; CHECK-NEXT:    [[Z1:%.*]] = add i32 [[X]], [[Y]]
; CHECK-NEXT:    br label [[BB_EXIT:%.*]]
; CHECK:       bb_false:
; CHECK-NEXT:    [[Z2:%.*]] = sub i32 [[X]], [[Y]]
; CHECK-NEXT:    [[COND2:%.*]] = icmp eq i32 [[Z2]], [[X]]
; CHECK-NEXT:    br i1 [[COND2]], label [[BB_TRUE:%.*]], label [[BB_EXIT:%.*]]
; CHECK:       bb_exit:
; CHECK-NEXT:    [[Z:%.*]] = mul i32 [[X]], [[Y]]
; CHECK-NEXT:    br label [[BB_ENTRY2:%.*]]
; CHECK:       bb_entry2:
; CHECK-NEXT:    [[A:%.*]] = add i32 [[X]], [[Z]]
; CHECK-NEXT:    br label [[BB_ENTRY3:%.*]]
; CHECK:       bb_entry3:
; CHECK-NEXT:    [[B:%.*]] = sub i32 [[X]], [[Z]]
; CHECK-NEXT:    [[COND3:%.*]] = icmp eq i32 [[A]], [[B]]
; CHECK-NEXT:    br i1 [[COND3]], label [[BB_TRUE2:%.*]], label [[BB_FALSE2:%.*]]
; CHECK:       bb_true2:
; CHECK-NEXT:    [[C:%.*]] = add i32 [[A]], [[A]]
; CHECK-NEXT:    br label [[BB_EXIT2:%.*]]
; CHECK:       bb_false2:
; CHECK-NEXT:    br label [[BB_EXIT2]]
; CHECK:       bb_exit2:
; CHECK-NEXT:    ret i32 [[A]]
;
  %cond = icmp eq i32 %x, %y
  br i1 %cond, label %bb_true, label %bb_false
bb_true:
  %z1 = add i32 %x, %y
  br label %bb_exit
bb_false:
  %z2 = sub i32 %x, %y
  %cond2 = icmp eq i32 %z2, %x
  br i1 %cond2, label %bb_true, label %bb_exit
bb_exit:
  %z = mul i32 %x, %y
  br label %bb_entry2
bb_entry2:
  %a = add i32 %x, %z
  br label %bb_entry3
bb_entry3:
  %b = sub i32 %x, %z
  %cond3 = icmp eq i32 %a, %b
  br i1 %cond3, label %bb_true2, label %bb_false2
bb_true2:
  %c = add i32 %a, %b
  br label %bb_exit2
bb_false2:
  br label %bb_exit2
bb_exit2:
  ret i32 %a
}