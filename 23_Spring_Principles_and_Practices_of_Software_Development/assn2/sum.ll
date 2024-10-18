define double @sum(double* %ptr, i32 %n) {
entry:
  %exit.entry = icmp eq i32 0, %n
  %zero = fadd double 0.0, 0.0
  %zero.fp128 = fpext double %zero to fp128 ; make fp128 type 0
  br i1 %exit.entry, label %for.cond.cleanup, label %for.body

for.body:
  ; ready ptr, idx, sum
  %sum = phi fp128 [ %sum.add, %for.body ], [ %zero.fp128, %entry ]
  %idx = phi i32 [ %idx.add1, %for.body ], [ 0, %entry ]
  %ptr.now = phi double* [ %ptr.now.add1 , %for.body], [ %ptr, %entry ]

  ; load double value, convert to fp128, then add
  %ptr.val = load double, double* %ptr.now
  %ptr.val.fp128 = fpext double %ptr.val to fp128
  %sum.add = fadd fp128 %sum, %ptr.val.fp128

  ; add 1 to idx and ptr. out if idx equal to n
  %ptr.now.add1 = getelementptr double, double* %ptr.now, i32 1
  %idx.add1 = add i32 %idx, 1
  %exit.for = icmp eq i32 %idx.add1, %n
  br i1 %exit.for, label %for.cond.cleanup, label %for.body

for.cond.cleanup:
  ; return fp128 value to double
  %ret.val.fp128 = phi fp128 [ %zero.fp128, %entry ], [ %sum.add, %for.body ]
  %ret.val = fptrunc fp128 %ret.val.fp128 to double
  ret double %ret.val
}
