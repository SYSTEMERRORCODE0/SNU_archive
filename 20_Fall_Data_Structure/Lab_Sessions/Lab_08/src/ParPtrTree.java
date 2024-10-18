import java.util.ArrayList;
import java.util.Arrays;

/**
 * General Tree class implementation for UNION/FIND
 */
public class ParPtrTree {
    private Integer[] array; // Node array
    private Integer[] size; // groupsize array. Consider only values of root nodes. We don't need to care others.
    private int maxSize = -999;

    public ParPtrTree(int maxsize) {
        this.maxSize = maxsize;
        array = new Integer[this.maxSize]; // Create node array
        size = new Integer[this.maxSize];
        for (int i = 0; i < this.maxSize; i++) {
            array[i] = null;
            size[i] = 1;
        }
    }

    public void clear() {
        array = new Integer[this.maxSize]; // Create node array
        size = new Integer[this.maxSize];
        for (int i = 0; i < this.maxSize; i++) {
            array[i] = null;
            size[i] = 1;
        }
    }

    /**
     * Determine if nodes are in different trees
     */
    public boolean differ(Integer a, Integer b) {
        //TODO: fill your code
        a = find(a);
        b = find(b);
        if(a == b) return false;
        else return true;
    }

    /**
     * Merge two subtrees using weighted union rule
     */
    public void union(Integer a, Integer b) {
        //TODO: fill your code
        // follow "weighted union rule"
        // if group size of two values are equal, hang b's root to a's.
        a = find(a);
        b = find(b);
        if(size[a] >= size[b]) {
            array[b] = a;
            size[a] += size[b];
        } else {
            array[a] = b;
            size[b] += size[a];
        }
    }

    /**
     * Find the root of the node using path compression
     */
    public Integer find(Integer curr) {
        //TODO: fill your code
        // use "path compression"
        Integer temp = curr;
        while(array[temp] != null) {
            temp = array[temp];
        }
        if(curr == temp) return temp;
        else {
            array[curr] = temp;
            return temp;
        }
    }

    /**
     * Return the size of the graph that the node belongs to
     */
    public Integer groupSize(Integer curr) {
        //TODO: fill your code
        curr = find(curr);
        return size[curr];
    }

    /**
     * Return the depth of the node
     */
    public Integer depth(Integer curr) {
        //TODO: fill your code
        if(array[curr] == null) return 0;
        else return depth(array[curr]) + 1;
    }

    /**
     * Summarize the current status of each tree
     */
    public void summary() {
        //TODO: fill your code
        ArrayList<Integer> single = new ArrayList<>();
        for(int i = 0; i < maxSize; i++) {
            if(array[i] == null) {
                if(size[i] != 1) {
                    System.out.println("Root: " + i + ", size: " + size[i]);
                } else {
                    single.add(i);
                }
            }
        }
        if(!single.isEmpty()) {
            System.out.print("Single node trees: ");
            for(int i = 0; i < single.size(); i++) {
                if(i != single.size()-1) System.out.print(single.get(i) + ", ");
                else System.out.println(single.get(i));
            }
        }
    }

    public Integer[] getSize() {
        return this.size;
    }

    public Integer[] getArray() {
        return this.array;
    }

    public void print() {
        System.out.println(Arrays.toString(array).replace("null", "N"));
    }
}
