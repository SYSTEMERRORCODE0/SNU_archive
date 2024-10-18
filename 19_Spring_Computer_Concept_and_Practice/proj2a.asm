;---------------------------------------------------;
; Skeleton LC-3 assembly code for Project #2A       ;
;---------------------------------------------------;
; Course: Computer Concept and Practice             ;
; Year: Spring 2019                                 ;
; Institution: Seoul National University            ;
; Department: Computer Science and Engineering      ;
;---------------------------------------------------;
; Instructor: Bryan S. Kim                          ;
; TA: Minwook Kim                                   ;
; Student: JunHyeok Kim                             ;
;---------------------------------------------------;
; Out: May 15th, 2019                               ;
; Due: June 5th, 2019                               ;
;---------------------------------------------------;

                .orig x3000
; initializing program
                ld      r4, gbl_ptr     ; global data
                ld      r5, lcl_ptr     ; local data
                add     r6, r5, #0      ; stack 
                jsr     main_start
                halt
gbl_ptr         .fill   gbl_data_start
lcl_ptr         .fill   xefff

; main
main_start      add     r6, r6, #-1
                str     r7, r6, #0		
                add     r6, r6, #-1
                str     r5, r6, #0      ; storing dyn link
                add     r5, r6, #-1     ; set new frame ptr
                add     r6, r6, #-1     ; int item @ lcl 0
                add     r6, r6, #-10    ; char cmd @ lcl -1 to -11
main_loop       ld      r0, main_prompt ; outputs '>'
                out
                ld      r2, main_negenter
                add     r3, r5, #-1      ; start of char cmd
main_input      getc
                out
                str     r0, r3, #0
                add     r3, r3, #-1
                add     r1, r0, r2
                brnp    main_input      ; if not newline, receive more char
                ldr     r0, r5, #-1     ; load cmd[0]
                ld      r1, main_negq
                add     r1, r0, r1
                brz     main_end
                ld      r1, main_negi
                add     r1, r0, r1
                brz     main_ins_start
                ld      r1, main_negr
                add     r1, r0, r1
                brz     main_rm_start
                ld      r1, main_negl
                add     r1, r0, r1
                brz     main_ls_start
                brnzp   main_loop
main_end        add     r6, r6, #11     ; pop local variable
                ldr     r5, r6, #0      
                add     r6, r6, #1      ; restore frame ptr
                ldr     r7, r6, #0
                add     r6, r6, #1      ; restore ret addr
                ret

; main: command is insert
main_ins_start  and     r0, r0, #0
                str     r0, r5, #0      ; write 0 to item
                add     r3, r5, #-3     ; load cmd[2]
main_ins_loop   ldr     r0, r3, #0
                add     r3, r3, #-1
                ld      r2, main_negenter
                add     r1, r0, r2
                brz     main_ins_chk
                ld      r2, main_negzero
                add     r0, r2, r0
                brn     main_ins_loop
                add     r1, r0, #-9
                brp     main_ins_loop
                ldr     r1, r5, #0      ; load item
                add     r1, r1, r1      ; 2*item
                add     r0, r1, r0      ; 2*item + newchar
                add     r1, r1, r1      ; 4*item
                add     r1, r1, r1      ; 8*item
                add     r0, r0, r1      ; 10*item + newchar
                str     r0, r5, #0      ; write new value
                brnzp   main_ins_loop
main_ins_chk    ldr     r0, r5, #0
                add     r6, r6, #-1 
                str     r0, r6, #0      ; push argument
                ld      r0, main_ins_ptr
                jsrr    r0
                ldr     r0, r6, #0      ; get return value
                add     r6, r6, #2
                and     r0, r0, r0      ; set CC
                brp     main_loop
                lea     r0, main_text_full
                puts
                brnzp   main_loop

; main: command is remove
main_rm_start   ld      r0, main_rm_ptr
                jsrr    r0
                ldr     r0, r6, #0      ; get return value
                add     r6, r6, #1
                and     r0, r0, r0      ; set CC
                brp     main_loop
                lea     r0, main_text_empty
                puts
                brnzp   main_loop

; main: command is list
main_ls_start   ld      r0, main_ls_ptr
                jsrr    r0
                brnzp   main_loop

main_prompt     .fill   x003e           ; ascii '>'
main_negr       .fill   xff8e           ; negation of ascii 'r'
main_negq       .fill   xff8f           ; negation of ascii 'q'
main_negl       .fill   xff94           ; negation of ascii 'l'
main_negi       .fill   xff97           ; negation of ascii 'i'
main_negzero    .fill   xffd0           ; negation of ascii '0'
main_negenter   .fill   xfff6           ; negation of ascii newline
main_text_full  .stringz "Insert failed\n"
main_text_empty .stringz "Remove failed\n"
main_ins_ptr    .fill   ins_start
main_rm_ptr     .fill   rm_start
main_ls_ptr     .fill   ls_start

; TODO: implement insert function
ins_start       add     r6, r6, #-1	;allocate return value
                and     r0, r0, #0	;initialize r0
				add		r6, r6, #-1
				str		r7, r6, #0	; store ret addr
				add		r6,	r6,	#-1	
				str		r5,	r6,	#0	; store dyn link
				add		r5, r6,	#-1	; set new frame pointer
				add		r6,	r6,	#-2	; push local variable, curr, next
				ldr		r2, r4, #0		; load heap_size
				add		r1,	r2, #-10	; 
				add		r1,	r1, #-10	; 
				brnp	ins_loop_start	; if(heap_size==MAX SIZE)	
                str     r0, r5, #3  ; return failure : prev : str r0, r6, #0
			    add     r6, r6, #2      ; pop local variable
                ldr     r5, r6, #0      
                add     r6, r6, #1      ; restore frame ptr
                ldr     r7, r6, #0
                add     r6, r6, #1      ; restore ret addr
                ret
ins_loop_start	add		r1,	r4,	#1	; getting addr of heap_arr[0]
				add		r1,	r1,	r2	; getting addr of heap_arr[heap_size]
				ldr		r3,	r5,	#4	; get item
				str		r3,	r1,	#0	; store item to heap_arr[heap_size]
				add		r2,	r2,	#1	; heap_size++
				str		r2,	r4,	#0	; store heap_size
				add		r0,	r2,	#-1	;
				str		r0,	r5,	#0	; curr=heap_size-1
				add		r2,	r0,	#0	; curr r0->r2
				and		r1,	r1,	#0	;;;;;;;;;;;;;;;;;;;
				add		r1,	r1,	#-1	;
ins_div2loop	add		r1,	r1,	#1	;	result of next=(curr-1)/2
				add		r2,	r2,	#-2	; 
				brp		ins_div2loop
				str		r1,	r5,	#-1	; store next
				ld      r2, ins_ls_ptr	
                jsrr    r2
ins_loop		ldr		r0, r5,	#0	;curr
				add		r0,	r0,	#0	
				brz		ins_end		; while(curr!=0)
				ldr		r1,	r5,	#-1 ;next
				add		r2,	r4,	#1	; getting addr of heap_arr[0]
				add		r2,	r2,	r1	; getting addr of heap_arr[next]
				add		r3,	r4,	#1	; getting addr of heap_arr[0]
				add		r3,	r3,	r0	; getting addr of heap_arr[curr]
				ldr		r0,	r2,	#0	; getting value of heap_arr[next]
				ldr		r1,	r3,	#0	; getting value of heap_arr[curr]
				not		r1,	r1
				add		r1,	r1,	#1
				add		r1,	r1,	r0
				brnz	ins_end		; if(heap_arr[curr]<heap_arr[next])
				ldr		r0,	r2,	#0	; getting value of heap_arr[next]
				str		r0,	r3,	#0	; heap_arr[curr] = heap_arr[next]
				ldr		r0,	r5,	#4	; get item
				str		r0,	r2,	#0	; heap_arr[next] = item
				ldr		r1,	r5,	#-1	; getting value of next
				str		r1,	r5, #0	; curr=next
				and		r0,	r0,	#0	;;;;;;;;;;;;;;;;;;;
				add		r0,	r0,	#-1	;
ins_div2loop2	add		r0,	r0,	#1	;	result of next=(curr-1)/2
				add		r1,	r1,	#-2	; 
				brp		ins_div2loop2
				str		r0,	r5,	#-1	; store next
				ld      r2, ins_ls_ptr	
                jsrr    r2
				brnzp	ins_loop
ins_end			and		r0,	r0,	#0
				add		r0,	r0,	#1
				str		r0,	r5,	#3		; store 1 to return value
		        add     r6, r6, #2      ; pop local variable
                ldr     r5, r6, #0      
                add     r6, r6, #1      ; restore frame ptr
                ldr     r7, r6, #0
                add     r6, r6, #1      ; restore ret addr
                ret
ins_ls_ptr      .fill   ls_start    ; use this to call heap_list()

; TODO: implement remove function
rm_start        add     r6, r6, #-1	;allocate return value
                and     r0, r0, #0	;initialize r0
				add		r6, r6, #-1
				str		r7, r6, #0	; store ret addr
				add		r6,	r6,	#-1	
				str		r5,	r6,	#0	; store dyn link
				add		r5, r6,	#-1	; set new frame pointer
				add		r6,	r6,	#-3	; push local variable, curr, next, temp
				ldr		r2, r4, #0	; load heap_size
				brnp	rm_loop_start	; if(heap_size==0)	
                str     r0, r5, #3  ; return failure
				add     r6, r6, #3      ; pop local variable
                ldr     r5, r6, #0      
                add     r6, r6, #1      ; restore frame ptr
                ldr     r7, r6, #0
                add     r6, r6, #1      ; restore ret addr
                ret
rm_loop_start	add		r0,	r4,	#1	; getting addr of heap_arr[0]
				ldr		r1,	r4,	#0	; load heap_size
				add		r1,	r1,	#-1	; --heap_size
				add		r2,	r0,	#0	; copy addr of heap_arr[0]
				add		r2,	r2,	r1	; addr of heap_arr[--heap_size]
				ldr		r2,	r2,	#0	; getting value of heap_arr[--heap_size]
				str		r2,	r0,	#0	; heap_arr[0]=heap_arr[--heap_size]
				str		r1,	r4,	#0	; store heap_size
				and		r0,	r0,	#0
				str		r0,	r5,	#0	; curr=0
				add		r0,	r0,	#1	; 
				str		r0, r5,	#-1 ; next=2*curr+1=1
				ld		r0,	rm_ls_ptr
				jsrr	r0				;heap_list()
rm_loop			ldr		r0,	r5,	#-1	; next
				ldr		r1,	r4,	#0	; heap_size
				not		r0,	r0
				add		r0,	r0,	#1
				add		r0,	r1,	r0	
				brnz	rm_end		;while(next<heap_size)
				ldr		r0,	r5,	#-1 ; next
				ldr		r1,	r4,	#0	; heap_size
				not		r0,	r0		; same as -(next+1)
				add		r0,	r0,	r1	; heap_size-(next+1)
				brnz	rm_loop_ifend	;&&
				ldr		r0,	r5,	#-1	; next
				add		r0,	r0,	#1	; next+1
				add		r1,	r4,	#1	; getting addr of heap_arr[0]
				add		r1,	r1,	r0	; getting addr of heap_arr[next+1]
				ldr		r0,	r1,	#0	; getting value of heap_arr[next+1]
				add		r1,	r1,	#-1	; getting addr of heap_arr[next]
				ldr		r1,	r1,	#0	; getting value of heap_arr[next]
				not		r0,	r0
				add		r0,	r0,	#1	
				add		r0,	r0,	r1	
				brnz	rm_loop_ifend	;heap_arr[next]-heap_arr[next+1]
				ldr		r0,	r5,	#-1	; next
				add		r0,	r0,	#1	; next+1
				str		r0,	r5,	#-1	; store next to next+1
rm_loop_ifend	ldr		r0,	r5,	#-1	; next
				add		r1,	r4,	#1	; getting addr of heap_arr[0]
				add		r2,	r1,	r0	; getting addr of heap_arr[next]
				ldr		r0,	r2,	#0	; getting value of heap_arr[next]
				ldr		r3,	r5,	#0	; curr
				add		r1,	r1,	r3	; getting addr of heap_arr[curr]
				ldr		r1,	r1,	#0	; getting value of heap_arr[curr]
				not		r0,	r0
				add		r0,	r0,	#1
				add		r0,	r1,	r0
				brnz	rm_end		; if (heap_arr[next]<heap_arr[curr])
				ldr		r0,	r5,	#-1	; next
				add		r1,	r4,	#1	; getting addr of haep_arr[0]
				add		r2,	r1,	r0	; getting addr of heap_arr[next]
				ldr		r2,	r2,	#0	; getting value of heap_arr[next]
				str		r2,	r5,	#-2	; store heap_arr[next] to temp
				add		r2,	r1,	r0	; getting addr of heap_arr[next]
				ldr		r0,	r5,	#0	; curr
				add		r3,	r1,	r0	; getting addr of heap_arr[curr]
				ldr		r3,	r3,	#0	; getting value of heap_arr[curr]
				str		r3,	r2,	#0	; heap_arr[next] = heap_arr[curr]
				ldr		r0,	r5,	#-2	; temp
				ldr		r2,	r5,	#0	; curr
				add		r3,	r1,	r2	; getting addr of heap_arr[curr]
				str		r0,	r3,	#0	; heap_arr[curr] = temp
				ldr		r0,	r5,	#-1	; next
				str		r0,	r5,	#0	; curr=next
				add		r0,	r0,	r0	; 2*curr
				add		r0,	r0,	#1	; 2*curr+1
				str		r0,	r5,	#-1	; next=2*curr+1
				ld		r0,	rm_ls_ptr
				jsrr	r0				;heap_list()
				brnzp	rm_loop
rm_end			and		r0,	r0,	#0
				add		r0,	r0,	#1
				str		r0,	r5,	#3		; store 1 to return value
		        add     r6, r6, #3      ; pop local variable
                ldr     r5, r6, #0      
                add     r6, r6, #1      ; restore frame ptr
                ldr     r7, r6, #0
                add     r6, r6, #1      ; restore ret addr
				ret
rm_ls_ptr       .fill   ls_start    ; use this to call heap_list()

; heap_list() 
ls_start        add     r6, r6, #-1
                str     r7, r6, #0      ; storing ret addr
                add     r6, r6, #-1
                str     r5, r6, #0      ; storing dyn link
                add     r5, r6, #-1     ; set new frame ptr
                add     r6, r6, #-1     ; push local variable, idx
                lea     r0, ls_text_heap
                puts
                ldr     r3, r4, #0
                brnp    ls_loop_start
                lea     r0, ls_text_empty
                puts
ls_loop_start   and     r2, r2, #0
                str     r2, r5, #0      ; init idx
                not     r3, r3
                add     r3, r3, #1
ls_loop         add     r1, r2, r3      ; idx-heapsize
                brzp    ls_end
                add     r1, r4, #1      ; getting addr of heap_arr[0]
                add     r1, r1, r2      ; getting addr of heap_arr[idx]
                ldr     r1, r1, #0
                jsr     print_start
                add     r2, r2, #1
                str     r2, r5, #0      ; update idx
                brnzp   ls_loop
ls_end          ld      r0, ls_newline
                out
                add     r6, r6, #1      ; pop local variable
                ldr     r5, r6, #0      
                add     r6, r6, #1      ; restore frame ptr
                ldr     r7, r6, #0
                add     r6, r6, #1      ; restore ret addr
                ret
ls_newline      .fill   x000a           ; ascii newline
ls_text_empty   .stringz "Empty"
ls_text_heap    .stringz "Heap: "

; helper subroutine for printing numbers
print_start     st      r7, print_saver7
                st      r3, print_saver3
                st      r2, print_saver2
                and     r3, r3, #0      ; internal use filter out leading zeros

                and     r0, r0, #0
                ld      r2, print_neg10k
print_10k_loop  add     r1, r2, r1
                brn     print_10k_done
                add     r0, r0, #1
                brnzp   print_10k_loop
print_10k_done  ld      r2, print_10k
                add     r1, r2, r1
                add     r3, r0, r3
                brz     print_1k_start  
                ld      r2, print_zero  
                add     r0, r2, r0
                out                     ; print char for 10k digit

print_1k_start  and     r0, r0, #0
                ld      r2, print_neg1k
print_1k_loop   add     r1, r2, r1
                brn     print_1k_done
                add     r0, r0, #1
                brnzp   print_1k_loop
print_1k_done   ld      r2, print_1k
                add     r1, r2, r1
                add     r3, r0, r3
                brz     print_1c_start
                ld      r2, print_zero
                add     r0, r2, r0
                out                     ; print char for the 1k digit

print_1c_start  and     r0, r0, #0
                ld      r2, print_neg1c
print_1c_loop   add     r1, r2, r1
                brn     print_1c_done
                add     r0, r0, #1
                brnzp   print_1c_loop
print_1c_done   ld      r2, print_1c
                add     r1, r2, r1
                add     r3, r0, r3
                brz     print_1d_start
                ld      r2, print_zero
                add     r0, r2, r0
                out                     ; print char for the 1c digit

print_1d_start  and     r0, r0, #0
print_1d_loop   add     r1, r1, #-10
                brn     print_1d_done
                add     r0, r0, #1
                brnzp   print_1d_loop
print_1d_done   add     r1, r1, #10
                add     r3, r0, r3
                brz     print_1_start
                ld      r2, print_zero
                add     r0, r2, r0
                out                     ; print char for the 1d digit

print_1_start   ld      r0, print_zero
                add     r0, r0, r1
                out                     ; print 1's digit
                ld      r0, print_space
                out                     ; print empty space
                ld      r2, print_saver2
                ld      r3, print_saver3
                ld      r7, print_saver7
                ret
print_saver7    .blkw   #1
print_saver3    .blkw   #1
print_saver2    .blkw   #1
print_neg10k    .fill   #-10000
print_neg1k     .fill   #-1000
print_neg1c     .fill   #-100
print_10k       .fill   #10000
print_1k        .fill   #1000
print_1c        .fill   #100
print_space     .fill   x20         ; ascii space
print_zero      .fill   x30         ; ascii '0'

gbl_data_start
; NOTE: we should not use heap_size and heap_arr in your code
heap_size       .blkw #1            ; R4(offset 0) points here
heap_arr        .blkw #100          ; R4(offset 1~101) points here
                .end