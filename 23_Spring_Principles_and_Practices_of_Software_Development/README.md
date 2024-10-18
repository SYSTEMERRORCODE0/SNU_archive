# 2023 1학기 소프트웨어 개발 원리 및 실습

## assn2

LLVM(컴파일러의 일종)을 이용하여 add, sum 함수를 구현

## assn3

### polygon.cpp

다각형의 넓이 구하는 코드. 본래 오버플로우가 일어나는 코드를 
오버플로우가 발생하지 않도록 수정하는 방식의 과제였다.

### unreachable.cpp

접근이 불가능한 코드 블럭을 그래프 탐색을 이용하여 사전 순으로 출력하는 코드를 작성하는 과제
llvm으로 중간 단계 컴파일된 내용을 cpp 코드로 최적화하는 방법에 대한 연습 과제이다.

## assn4

'icmp eq iN x, y' : N-bit 정수 x와 y가 같으면 true, 아니면 false (llvm 코드)

위의 명령으로 얻은 true/false 값을 이용하여 branch를 할 때, 항상 true나 false일 경우,

접근할 수 없는 코드 블럭을 제거(dominate)하는 최적화 코드(cpp)를 작성하는 과제이다.

mycheck 폴더 내의 코드는 직접 만든 테스트케이스 및 체킹 코드이다(llvm).

## Project

3인 1조로 주어진 'Weird Machine(명령어의 cost를 임의로 정함)'에 맞는 LLVM 최적화 코드(cpp)를 작성하는

프로젝트이다. 코드는 비공개이며, 경합 이전 주어진 예시 테스트케이스 기준으로 약 42%의 cost 감소를 이루었다.