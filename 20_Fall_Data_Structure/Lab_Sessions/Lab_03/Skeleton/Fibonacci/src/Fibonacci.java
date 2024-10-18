
public class Fibonacci {

    /**
     * Compute the nth number of Fibonacci sequence.
     * Notice: F(0) = 0 and F(1) = 1;
     * @param N
     * @return the nth Fibonacci number.
     */
    public static int computeFibonacci(int N) {
        if (N > 40)
            throw new AssertionError("Number is too large!");
        // TODO Fill your code to compute the nth Fibonacci number
        if (N == 0) return 0;
        if (N == 1) return 1;
        return computeFibonacci(N - 1) + computeFibonacci(N - 2);
    }

    /**
     * Print Fibonacci sequence with length of n.
     * @param N
     */
    public static void drawFibonacci(int N) {
        // TODO Fill your code to print the Fibonacci sequence.
        // Hint: Use computeFibonacci method.
        for(int i = 0; i < N; i++) {
            System.out.print(computeFibonacci(i) + " ");
        }
        System.out.println();
    }
}
