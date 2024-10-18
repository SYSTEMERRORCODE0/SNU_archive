//------------------------------------------------------------------------------
//
// memtrace
//
// trace calls to the dynamic memory manager
//
#define _GNU_SOURCE

#include <dlfcn.h>
#include <stdio.h>
#include <stdlib.h>
#include <assert.h>
#include <memlog.h>
#include <memlist.h>

//
// function pointers to stdlib's memory management functions
//
static void *(*mallocp)(size_t size) = NULL;
static void (*freep)(void *ptr) = NULL;
static void *(*callocp)(size_t nmemb, size_t size);
static void *(*reallocp)(void *ptr, size_t size);

//
// statistics & other global variables
//
static unsigned long n_malloc  = 0;
static unsigned long n_calloc  = 0;
static unsigned long n_realloc = 0;
static unsigned long n_allocb  = 0;
static unsigned long n_freeb   = 0;
static item *list = NULL;

//
// init - this function is called once when the shared library is loaded
//
__attribute__((constructor))
void init(void)
{
  char *error;

  /* malloc */
  if(!mallocp) {
    mallocp = dlsym(RTLD_NEXT, "malloc");
    if((error = dlerror()) != NULL) {
      fputs(error, stderr);
      exit(1);
    }
  }

  /* calloc */
  if(!callocp) {
    callocp = dlsym(RTLD_NEXT, "calloc");
    if((error = dlerror()) != NULL) {
      fputs(error, stderr);
      exit(1);
    }
  }

  /* realloc */
  if(!reallocp) {
    reallocp = dlsym(RTLD_NEXT, "realloc");
    if((error = dlerror()) != NULL) {
      fputs(error, stderr);
      exit(1);
    }
  }

  /* free */
  if(!freep) {
    freep = dlsym(RTLD_NEXT, "free");
    if((error = dlerror()) != NULL) {
      fputs(error, stderr);
      exit(1);
    }
  }

  LOG_START();

  // initialize a new list to keep track of all memory (de-)allocations
  // (not needed for part 1)
  list = new_list();

  // ...
}

void *malloc(size_t size) {

  void *res;

  res = mallocp(size);
  n_allocb += (unsigned long) size;
  n_malloc++;

  alloc(list, res, size);

  LOG_MALLOC(size, res);

  return res;
}

void *calloc(size_t nmemb, size_t size) {
  
  void *res;
  unsigned long total_size;

  res = callocp(nmemb, size);
  total_size = (unsigned long) nmemb * (unsigned long) size;
  n_allocb += total_size;
  n_calloc++;

  alloc(list, res, (size_t) total_size);

  LOG_CALLOC(nmemb, size, res);

  return res;
}

void *realloc(void *ptr, size_t size) {
  
  void *res;
  item *cur;

  // Finding ptr before reallocation
  cur = find(list, ptr);
  if(cur == NULL) {
    res = mallocp(size);
    LOG_REALLOC(ptr, size, res);
    LOG_ILL_FREE();
  } else if(cur->cnt == 0) {
    res = mallocp(size);
    LOG_REALLOC(ptr, size, res);
    LOG_DOUBLE_FREE();
  } else {
    cur = dealloc(list, ptr);
    n_freeb += (unsigned long) cur->size;

    res = reallocp(ptr, size);
    LOG_REALLOC(ptr, size, res);
  }

  n_allocb += (unsigned long) size;
  n_realloc++;

  alloc(list, res, size);

  return res;
}

void free(void *ptr) {
  
  item *cur;

  LOG_FREE(ptr);

  // Finding ptr before free
  cur = find(list, ptr);
  if(cur == NULL) {
    LOG_ILL_FREE();
    return;
  } else if(cur->cnt == 0) {
    LOG_DOUBLE_FREE();
    return;
  }
  
  cur = dealloc(list, ptr);
  n_freeb += cur->size;

  freep(ptr);

}

//
// fini - this function is called once when the shared library is unloaded
//
__attribute__((destructor))
void fini(void)
{
  // ...

  LOG_STATISTICS(n_allocb, n_allocb / (n_malloc + n_calloc + n_realloc), n_freeb);

  if(n_allocb > n_freeb) {
    LOG_NONFREED_START();
    item *i;
    i = list->next;
    while(i != NULL) {
      if(i->cnt > 0) LOG_BLOCK(i->ptr, i->size, i->cnt);
      i = i->next;
    }
  }

  LOG_STOP();

  // free list (not needed for part 1)
  free_list(list);
}

// ...
