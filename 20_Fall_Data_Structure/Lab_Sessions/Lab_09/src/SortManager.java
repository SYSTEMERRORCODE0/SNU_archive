import java.net.PasswordAuthentication;
import java.util.concurrent.TimeUnit;

public class SortManager {
    private int MAX_NUM;
    private Node<Integer, String>[] items;
    int N = -1;

    public SortManager() {
        MAX_NUM = 999;
        items = new Node[MAX_NUM];
    }

    /**
     * Input: line of items
     * Set items in the line.
     * Print list of items by calling 'print' function at the end.
     * Hint: use "String".split(" ") to split each item
     * use "String".split("_") to split key and item
     * use Integer.parseInt("String") to convert "String" into a integer.
     */
    public void setItems(int n, String itemLine) {
        this.N = n;
        String[] newItems = itemLine.split(" ");
        ///TODO: fill in the code
        items = new Node[MAX_NUM];
        for(int i = 0; i < this.N; i++) {
            String[] item = newItems[i].split("_");
            items[i] = new Node<>(Integer.parseInt(item[0]), item[1]);
        }
        print();
    }

    /**
     * Sort the items in the "items" array.
     * Print list of items by calling 'print' function at the end.
     * Hint. you have to compare Integer type values with 'Integer.compareTo(Competitor)' function.
     * Hint. you can also use 'print' function for debugging.
     */
    public void doBubbleSort() {
        ///TODO: fill in this code
        for(int i = this.N; i > 0; i--) {
            for(int j = 1; j < i; j++) {
                if(items[j-1].getKey().compareTo(items[j].getKey()) > 0) {
                    Node<Integer, String> temp = items[j-1];
                    items[j-1] = items[j];
                    items[j] = temp;
                }
            }
        }
        print();
    }


    /**
     * Sort the items in the "items" array.
     * Print list of items by calling 'print' function at the end.
     * Hint. you have to compare Integer type values with 'Integer.compareTo(Competitor)' function.
     * Hint. you can also use 'print' function for debugging.
     */
    public void doSelectionSort() {
        for (int i = 0; i < this.N; i++) {
            int minKey = 99999;
            int minIndex = -1;
            for (int j = i; j < this.N; j++) {
                if (items[j].getKey().compareTo(minKey) < 0) {
                    minIndex = j;
                    minKey = items[j].getKey();
                }
            }

            Node<Integer, String> temp = items[minIndex];
            items[minIndex] = items[i];
            items[i] = temp;
        }
        print();
    }


    /**
     * Sort the items in the "items" array keeping your array stable.
     * Print list of items by calling 'print' function at the end.
     * Hint. you have to compare Integer type values with 'Integer.compareTo(Competitor)' function.
     * Hint. you can also use 'print' function for debugging.
     */
    public void doStableSelectionSort() {
        ///TODO: fill in this code
        for(int i = 0; i < this.N; i++) {
            int minKey = 99999;
            int minIndex = -1;
            for (int j = i; j < this.N; j++) {
                if (items[j].getKey().compareTo(minKey) < 0) {
                    minIndex = j;
                    minKey = items[j].getKey();
                }
            }

            for(int j = minIndex; j > i; j--) {
                Node<Integer, String> temp = items[j];
                items[j] = items[j-1];
                items[j-1] = temp;
            }
        }
        print();
    }


    /**
     * Print the list of nodes in the 'this.items'.
     * You should use 'Node.toString()' when you print key and item of the node.
     * e.g. System.out.println(items[i].toString())
     */
    public void print() {
        if (this.N == -1) {
            System.out.println("There is no items to print");
        }
        ///TODO: fill in the code
        System.out.print("ITEMS: ");
        for(int i = 0; i < this.N; i++) {
            System.out.print(items[i].toString());
        }
        System.out.println();
    }

    /**
     * Check 'this.items' is sorted and if it was sorted with the stable sorting method.
     * Print "CHECK: Unsorted" if "this.items" are not sorted
     * Print "CHECK: Sorted, but not stable" if "this.items" are sorted but not stable.
     * Print "CHECK: Sorted and stable." if "this.items" are both sorted and stable.
     * Assume, all items are given lexicographical order at first  and there are no duplicate items.
     * Thus, two items with same keys, but not following the lexicographical order means that sorting method wasn't stable.
     */
    public void check() {
        ///TODO: fill in the code
        boolean stable = true;
        for(int i = 1; i < this.N; i++) {
            if(items[i-1].getKey().compareTo(items[i].getKey()) == 0 && items[i-1].getItem().compareTo(items[i].getItem()) > 0) {
                stable = false;
            }
            if(items[i-1].getKey().compareTo(items[i].getKey()) > 0) {
                System.out.println("CHECK: Unsorted.");
                return;
            }
        }
        if(stable) {
            System.out.println("CHECK: Sorted and stable.");
        } else {
            System.out.println("CHECK: Sorted, but not stable.");
        }
    }
}
