# 2023 1학기 시스템 프로그래밍

### Lab01

C언어와 stdlib의 메모리 할당 관련 라이브러리를 이용하여 

메모리 할당과 관련된 함수(malloc, calloc, realloc, free)를 구현하고

할당되거나 free된 메모리를 Trace하는 기능 및 할당되지 않은 메모리를 free하거나(illegal free) 

이미 free한 메모리를 free하는(double free)하는 경우를 잡아내고 무시하는 기능을 추가한다.

폴더 내 lab1.pdf 참조

### Lab02

C언어를 이용하여 프로세스를 foreground, background로 나누어 동작시키는 함수,

foreground 프로세스의 동작 완료를 기다리는 함수,

SIGINT, SIGTSTP 등의 시그널을 통해 프로세스를 멈추는 등의 동작을 수행하는 핸들러 함수 등을 구현하여

프로세스 실행과 wait, 시그널을 통한 동작 변화를 이해하는 과제였다.

폴더 내 lab2.pdf 참조

### Lab03

C언어를 이용하여 할당 메모리 블록의 구조를 직접 구성하고,

포인터와 크기를 직접 할당하여 malloc, free, realloc 함수를 구현한다.

이때 최대한 효율적인 할당 방식을 이용 또는 고안하는 것이 이 과제의 목표이기도 하다.

폴더 내 lab3.pdf 참조

### Lab04

ptree 폴더 : C언어를 이용하여 프로세스 ID로부터 프로세스 트리를 Trace하는 프로그램을 구현

paddr 폴더 : C언어를 이용하여 Virtual Address를 이용해서 Physical Address를 구하는 프로그램을 구현

이 프로그램들을 kernel에 모듈로 넣어 작동시켜보는 과제였다.

폴더 내 lab4.pdf 참조

### Lab05

C언어로 웹 오브젝트를 받아오는 간단한 HTTP 프록시를 구현한다.

다수의 concurrent한 요청을 처리하고, caching까지 구현하는 것이 과제의 목표였다.

폴더 내 lab5.pdf 참조
