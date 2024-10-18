/*
|---------------------------------------------------|
| C reference code for Project #2A                  |
|---------------------------------------------------|
| Course: Computer Concept and Practice             |
| Year: Spring 2019                                 |
| Institution: Seoul National University            |
| Department: Computer Science and Engineering      |
|---------------------------------------------------|
| Instructor: Bryan S. Kim                          |
| TA: Minwook Kim                                   |
| Student: JunHyeok Kim                             |
|---------------------------------------------------|
| Out: May 15th, 2019                               |
| Due: June 5th, 2019                               |
|---------------------------------------------------|
*/

#include <stdio.h>
#define MAX_SIZE 20
#define SUCCESS 1
#define FAILURE 0

int heap_arr[MAX_SIZE];
int heap_size;

int heap_insert(int item);
int heap_remove();
void heap_list();

int main(){
    int item;
    char cmd[10];

    while(1){
        printf(">");
        scanf("%s", cmd);
        if (cmd[0]=='q') break;
        else if (cmd[0]=='i'){
            scanf("%d", &item);
            if (!heap_insert(item)){
                printf("Insert failed\n");
            }
        }
        else if (cmd[0]=='r'){
            if (!heap_remove()){
                printf("Remove failed\n");
            }
        }
        else if (cmd[0]=='l'){
            heap_list();
        }
    }
    return SUCCESS;
}

int heap_insert(int item){
    int curr, next;
    
    if (heap_size==MAX_SIZE){
        return FAILURE;
    }

    heap_arr[heap_size++] = item;

    curr = heap_size-1;
    next = (curr-1)/2;
    heap_list();
    while(curr!=0){
        if (heap_arr[curr]<heap_arr[next]){
            heap_arr[curr] = heap_arr[next];
            heap_arr[next] = item;
            curr = next;
            next = (curr-1)/2;
            heap_list();
        }else{
            break;
        }
    }
    return SUCCESS;
}

int heap_remove(){
    int curr, next, temp;

    if (heap_size==0){
        return FAILURE;
    }

    heap_arr[0] = heap_arr[--heap_size];

    curr = 0;
    next = 2*curr+1;
    heap_list();
    while(next<heap_size){
        if (next+1<heap_size && heap_arr[next+1]<heap_arr[next]){
            next += 1;
        }
        if (heap_arr[next]<heap_arr[curr]){
            temp = heap_arr[next];
            heap_arr[next] = heap_arr[curr];
            heap_arr[curr] = temp;
            curr = next;
            next = 2*curr+1;
            heap_list();
        }else{
            break;
        }
    }
    return SUCCESS;
}

void heap_list(){
    int idx;
    printf("Heap: ");
    if (heap_size==0){
        printf("Empty");
    }
    for (idx=0; idx<heap_size; idx+=1){
        printf("%d ", heap_arr[idx]);
    }
    printf("\n");
}