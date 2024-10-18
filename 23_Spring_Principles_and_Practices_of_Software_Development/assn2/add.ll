define void @add(i32* %ptr1, i32* %ptr2, i32* %val) {
entry:
  %ptr1.val = load i32, i32* %ptr1
  %ptr2.val = load i32, i32* %ptr2
  %val.val = load i32, i32* %val

  %ptr1.add.val = add i32 %ptr1.val, %val.val
  %ptr2.add.val = add i32 %ptr2.val, %val.val

  store i32 %ptr1.add.val, i32* %ptr1
  store i32 %ptr2.add.val, i32* %ptr2

  ret void
}
