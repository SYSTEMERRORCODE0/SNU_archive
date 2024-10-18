/*
 * mm-2019-18499.c - fast malloc package that using Explicit Freed List 
 *                                                & Insertion sort(descending) 
 *                                                & best fit
 *                                                & optimized realloc
 * 
 * In this package, Only freed block is in the list, and connected with pointer
 * in the block(prev, next).
 * A freed block has Header, Prev (pointer), Next(pointer), and Footer.
 * A allocated block has Header, Payload, and Footer
 * Blocks are always coalesced or reused when possible. 
 * Realloc reuses the previously allocated block if possible,
 * but using mm_malloc and mm_free when they are not possible.
 *
 */
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <unistd.h>
#include <string.h>

#include "mm.h"
#include "memlib.h"

/*********************************************************
 * NOTE TO STUDENTS: Before you do anything else, please
 * provide your team information in the following struct.
 ********************************************************/

/* single word (4) or double word (8) alignment */
#define ALIGNMENT 8

/* rounds up to the nearest multiple of ALIGNMENT */
#define ALIGN(size) (((size) + (ALIGNMENT-1)) & ~0x7)


#define SIZE_T_SIZE (ALIGN(sizeof(size_t)))



#define VALUE_SIZE_T *(size_t *)
#define VALUE_VOID_PTR *(void **)
#define HEADER(ptr) ptr
#define PREV(ptr) (void *)((char *)ptr + SIZE_T_SIZE)
#define NEXT(ptr) (void *)((char *)ptr + 2 * SIZE_T_SIZE)
#define PAYLOAD(ptr) (void *)((char *)ptr + SIZE_T_SIZE)
#define FOOTER(ptr) (void *)((char *)ptr + (VALUE_SIZE_T(ptr) & -2) - SIZE_T_SIZE)
#define ALLOCATED(ptr) VALUE_SIZE_T(ptr) & 1

static void *head_ptr;
static void *tail_ptr;

/*
 *    Structure
 *
 *    -> Allocated Block
 *      8 bytes                        8 * N bytes                          8 bytes                  
 *    +--------+----------------------------------------------------------+--------+
 *    | HEADER |                         PAYLOAD                          | FOOTER |
 *    +--------+----------------------------------------------------------+--------+
 *
 *    -> Freed Block
 *      8 bytes  8 bytes  8 bytes                8 * N bytes                8 bytes
 *    +--------+--------+--------+----------------------------------------+--------+
 *    | HEADER |  PREV  |  NEXT  |                                        | FOOTER |
 *    +--------+--------+--------+----------------------------------------+--------+
 */




/* remove block from the linked list */
static void remove_block(void *ptr)
{
    VALUE_VOID_PTR(NEXT(VALUE_VOID_PTR(PREV(ptr)))) = VALUE_VOID_PTR(NEXT(ptr));    // next of prev -> next
    if(VALUE_VOID_PTR(NEXT(ptr)) < mem_heap_hi()) {
        VALUE_VOID_PTR(PREV(VALUE_VOID_PTR(NEXT(ptr)))) = VALUE_VOID_PTR(PREV(ptr));    // prev of next -> prev (if next is not end)
    } else {
        /* if remove from tail, move tail to prev */
        tail_ptr = VALUE_VOID_PTR(PREV(ptr));
    }
}

/* insert block to the linked list, next to "next_to" */
static void insert_block(void *ptr, void *next_to)
{
    if(VALUE_VOID_PTR(NEXT(next_to)) < mem_heap_hi()) {
        VALUE_VOID_PTR(PREV(VALUE_VOID_PTR(NEXT(next_to)))) = HEADER(ptr);  // prev of next -> prev (if next is not end)
    } else {
        /* if insert next to tail, move tail to ptr */
        tail_ptr = HEADER(ptr);
    }
    VALUE_VOID_PTR(PREV(ptr)) = HEADER(next_to);    // prev of ptr -> prev

    VALUE_VOID_PTR(NEXT(ptr)) = VALUE_VOID_PTR(NEXT(next_to));  // next of ptr -> next
    VALUE_VOID_PTR(NEXT(next_to)) = HEADER(ptr);    // next of prev -> ptr
}

/* try coalescing, do nothing if can't */
static void *try_coalesce_next(void *ptr) 
{
    /* next : not a next block in linked list, but an adjacent next block */
    void *next = (void *)((char *)ptr + VALUE_SIZE_T(HEADER(ptr)));

    if((next < mem_heap_hi()) && (VALUE_SIZE_T(next) & 1) == 0) {

        /* remove quickly from list for avoid error */
        remove_block(ptr);
        /* where to put new empty block, next to */
        void *next_to = VALUE_VOID_PTR(PREV(next));
        
        VALUE_SIZE_T(HEADER(ptr)) = VALUE_SIZE_T(ptr) + VALUE_SIZE_T(next);  //front

        remove_block(next);
        insert_block(ptr, next_to);

        VALUE_SIZE_T(FOOTER(next)) = VALUE_SIZE_T(ptr);   //back (of next)

        return ptr;
    }
    return NULL;
}

/* try coalescing, do nothing if can't */
static void *try_coalesce_prev(void *ptr)
{
    /* prev : not a prev block in linked list, but an adjacent prev block */
    void *prev_footer = (void *)((char *)ptr - SIZE_T_SIZE);
    void *prev = (void *)((char *)prev_footer - (VALUE_SIZE_T(prev_footer) & -2) + SIZE_T_SIZE);
    
    if((prev > mem_heap_lo()) && (VALUE_SIZE_T(prev) & 1) == 0) {

        VALUE_SIZE_T(FOOTER(ptr)) = VALUE_SIZE_T(ptr) + VALUE_SIZE_T(prev);   //back

        remove_block(ptr);
        /* there's no need to re-insert prev block*/

        VALUE_SIZE_T(HEADER(prev)) = VALUE_SIZE_T(ptr) + VALUE_SIZE_T(prev);  //front (of prev)
        return prev;
    }
    return NULL;
}

/* insert block next to root */
static void insert_root(void *ptr)
{
    insert_block(ptr, head_ptr);
}

/* "SORT" is order by descending of memory size */
/* move block to next continuously (insertion sort) */
static void sort_next(void *ptr)
{
    /* remove quickly from list for avoid error */
    remove_block(ptr);

    void *move_next_to = VALUE_VOID_PTR(PREV(ptr));
    size_t size = VALUE_SIZE_T(HEADER(ptr)) & -2;

    while(VALUE_VOID_PTR(NEXT(move_next_to)) < mem_heap_hi() && VALUE_SIZE_T(VALUE_VOID_PTR(NEXT(move_next_to))) > size) {
        move_next_to = VALUE_VOID_PTR(NEXT(move_next_to));
    }

    insert_block(ptr, move_next_to);
}

/* move block to prev continuously (insertion sort) */
static void sort_prev(void *ptr)
{
    void *move_next_to = VALUE_VOID_PTR(PREV(ptr));
    size_t size = VALUE_SIZE_T(HEADER(ptr)) & -2;

    while(move_next_to > mem_heap_lo() && VALUE_SIZE_T(HEADER(move_next_to)) < size) {
        move_next_to = VALUE_VOID_PTR(PREV(move_next_to));
    }

    remove_block(ptr);
    insert_block(ptr, move_next_to);
}

/* 
 * mm_init - initialize the malloc package.
 *           make a 4-byte block for head of linked list
 */
int mm_init(void)
{
    void *p = mem_sbrk(4 * SIZE_T_SIZE);
    VALUE_SIZE_T(HEADER(p)) = 4 * SIZE_T_SIZE;
    VALUE_VOID_PTR(PREV(p)) = mem_heap_lo();
    VALUE_VOID_PTR(NEXT(p)) = mem_heap_hi();
    VALUE_SIZE_T(FOOTER(p)) = 4 * SIZE_T_SIZE;
    head_ptr = tail_ptr = mem_heap_lo();
    
    return 0;
}

/* 
 * mm_malloc - Allocate a block by incrementing the brk pointer.
 *     Always allocate a block whose size is a multiple of the alignment.
 */
void *mm_malloc(size_t size)
{
    /* bidirectional + next, prev pointer */
    size_t newsize = ALIGN(size + SIZE_T_SIZE * 2);
    if(newsize <= 4 * SIZE_T_SIZE) newsize = 4 * SIZE_T_SIZE;

    /* best fit */
    void *p = mem_heap_lo();
    while((VALUE_VOID_PTR(NEXT(p)) < mem_heap_hi()) && VALUE_SIZE_T(VALUE_VOID_PTR(NEXT(p))) >= newsize) {
        p = VALUE_VOID_PTR(NEXT(p));
    }

    /* No space, make a new Space of size Pagesize or newsize */
    if(p == mem_heap_lo()) {
        void *new;
        size_t sbrk_size = mem_pagesize();
        if(newsize > sbrk_size)
            sbrk_size = newsize;

        new = mem_sbrk(sbrk_size);
        VALUE_VOID_PTR(NEXT(tail_ptr)) = mem_heap_hi();

        if (new == (void *)-1)
	        return NULL;
        else {
            /* make space */
            VALUE_SIZE_T(HEADER(new)) = sbrk_size;   // front

            insert_root(new);

            VALUE_SIZE_T(FOOTER(new)) = sbrk_size; //back
            
            p = HEADER(new);
        }
    }
    
    /* There is space*/
    size_t oldsize = VALUE_SIZE_T(p) & -2;

    /* if split block cannot be made, give it more little space */
    if(newsize + 4 * SIZE_T_SIZE > oldsize) newsize = oldsize;

    VALUE_SIZE_T(HEADER(p)) = newsize | 1; //front 
    VALUE_SIZE_T(FOOTER(p)) = newsize | 1; //back

    /* if there will be split */
    if(newsize < oldsize) {
        void *split_ptr = (void *)((char *)p + newsize);
        void *next_to = VALUE_VOID_PTR(PREV(p));

        VALUE_SIZE_T(HEADER(split_ptr)) = oldsize - newsize;   //splitted front

        remove_block(p);
        insert_block(split_ptr, next_to);

        VALUE_SIZE_T(FOOTER(split_ptr)) = oldsize - newsize; //splitted back

        sort_next(split_ptr);

    } else {
        remove_block(p);
    }
    
    return PAYLOAD(p);
}

/*
 * mm_free - Freeing a block does nothing.
 */
void mm_free(void *ptr)
{
    ptr = (void *)((char *)ptr - SIZE_T_SIZE);

    VALUE_SIZE_T(HEADER(ptr)) = VALUE_SIZE_T(HEADER(ptr)) & -2;   //front
    VALUE_SIZE_T(FOOTER(ptr)) = VALUE_SIZE_T(HEADER(ptr));  //back
    insert_root(ptr);

    /* coalesce both */
    void *p;
    if((p = try_coalesce_next(ptr)) != NULL) ptr = p;
    if((p = try_coalesce_prev(ptr)) != NULL) ptr = p;

    /* either one of this will not work*/
    sort_next(ptr); 
    sort_prev(ptr);
}

/*
 * mm_realloc - Implemented simply in terms of mm_malloc and mm_free
 */
void *mm_realloc(void *ptr, size_t size)
{
    /* if ptr is null, run mm_malloc */
    if(ptr == NULL) {
        return mm_malloc(size);
    }

    /* if size is 0, run mm_free */
    if(size == 0) {
        mm_free(ptr);
        return NULL;
    }

    void *oldptr = (void *)((char *)ptr - SIZE_T_SIZE);
    void *newptr = oldptr;
    
    size_t newsize = ALIGN(size + SIZE_T_SIZE * 2);
    size_t blockSize = VALUE_SIZE_T(oldptr) & -2;
    size_t copySize = blockSize - 2 * SIZE_T_SIZE;

    /* if size is less than before, just change the size */
    if(newsize <= blockSize) {
        /* if split block cannot be made, give it more little space */
        if(newsize + 4 * SIZE_T_SIZE > blockSize) newsize = blockSize;

        VALUE_SIZE_T(HEADER(newptr)) = newsize | 1; //front 
        VALUE_SIZE_T(FOOTER(newptr)) = newsize | 1; //back

        /* */
        if(newsize < blockSize) {

            void *split_ptr = (void *)((char *)newptr + newsize);

            VALUE_SIZE_T(HEADER(split_ptr)) = blockSize - newsize;   //splitted front

            insert_root(split_ptr);
            /* If there is another space next to split block */
            void *p;
            if((p = try_coalesce_next(split_ptr)) != NULL) split_ptr = p;

            VALUE_SIZE_T(FOOTER(split_ptr)) = blockSize - newsize; //splitted back

            sort_next(split_ptr);
        }
        return PAYLOAD(newptr);
    }

    void *next = (void *)((char *)oldptr + (VALUE_SIZE_T(oldptr) & -2));  //next block

    /* if next block is empty and additional size is OK, Use the block */
    if(next < mem_heap_hi() && (VALUE_SIZE_T(next) & 1) == 0) {

        /* There is enough space in next block */
        if(blockSize + VALUE_SIZE_T(next) >= newsize) {
            if(newsize + 4 * SIZE_T_SIZE > VALUE_SIZE_T(next) + blockSize) newsize = VALUE_SIZE_T(next) + blockSize;

            /* remove the next block early */
            remove_block(next);

            size_t additional_size = newsize - blockSize;

            /* There will be split block */
            if(additional_size < VALUE_SIZE_T(next)) {
                void *split_ptr = (void *)((char *)newptr + newsize);

                VALUE_SIZE_T(HEADER(split_ptr)) = VALUE_SIZE_T(next) - additional_size;   //splitted front

                insert_root(split_ptr);

                VALUE_SIZE_T(FOOTER(split_ptr)) = VALUE_SIZE_T(next) - additional_size; //splitted back

                sort_next(split_ptr);
            }

            VALUE_SIZE_T(HEADER(newptr)) = newsize | 1; //front 
            VALUE_SIZE_T(FOOTER(newptr)) = newsize | 1; //back

            return PAYLOAD(newptr);
        } else if((void *)((char *)next + VALUE_SIZE_T(next)) >= mem_heap_hi()) {
            /* There is not enough space in next block, but next is the end of heap */
            size_t additional_size = newsize - blockSize - VALUE_SIZE_T(next);

            /* remove the block early*/
            remove_block(next);
            /* make exact need memory */
            mem_sbrk(additional_size);
            VALUE_VOID_PTR(NEXT(tail_ptr)) = mem_heap_hi();

            VALUE_SIZE_T(HEADER(newptr)) = newsize | 1; //front 
            VALUE_SIZE_T(FOOTER(newptr)) = newsize | 1; //back

            return PAYLOAD(newptr);
        }
    }

    /* The normal cases, that means normally malloc then free*/
    newptr = mm_malloc(size);
    newptr = (void *)((char *)newptr - SIZE_T_SIZE);

    if (newptr == NULL)
      return NULL;
    
    memcpy(PAYLOAD(newptr), PAYLOAD(oldptr), copySize);
    mm_free(PAYLOAD(oldptr));
    return PAYLOAD(newptr);
}