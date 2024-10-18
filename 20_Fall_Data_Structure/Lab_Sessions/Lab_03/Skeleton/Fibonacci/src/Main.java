import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        while (sc.hasNext()) {
            String command = sc.next();

            if ("number".equals(command)) {
                int n = sc.nextInt();

                // TODO Fill your code to compute and print a binomial coefficient.
                Fibonacci fibonacci = new Fibonacci();
                System.out.println(fibonacci.computeFibonacci(n));

            } else if ("print".equals(command)) {
                int n = sc.nextInt();

                //TODO Fill your code to print the Fibonacci sequence.
                Fibonacci fibonacci = new Fibonacci();
                fibonacci.drawFibonacci(n);

            } else {
                throw new AssertionError("Invalid input!");
            }
        }
    }

}
