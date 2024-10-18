import java.util.Scanner;

public class Main {

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);

        while (sc.hasNext()) {
            String command = sc.next();

            if ("binomial".equals(command)) {
                int n = sc.nextInt();
                int k = sc.nextInt();

                // TODO Fill your code to compute and print a binomial coefficient.
                PascalTriangle pascalTriangle = new PascalTriangle();
                System.out.println(n + "C" + k + " = " + pascalTriangle.computeBinomialCoef(n, k));

            } else if ("draw".equals(command)) {
                int n = sc.nextInt();

                // TODO Fill your code to print a Pascal's triangle.
                PascalTriangle pascalTriangle = new PascalTriangle();
                pascalTriangle.drawPascalTriangle(n);

            } else {
                throw new AssertionError("Invalid input!");
            }
        }
    }

}
