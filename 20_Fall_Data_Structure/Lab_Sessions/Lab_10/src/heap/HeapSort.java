package heap;

import java.util.Arrays;

public class HeapSort<E extends Comparable<? super E>> {
    private MaxHeap<E> maxHeap;
    private int n;
    private E[] array;

    private static final int SORT_A = 2;
    private static final int SORT_D = 3;

    public HeapSort(int n){
        array = newArray(n);
        maxHeap = new MaxHeap<E>(array, 0, n);
        this.n = n;
    }

    public void add(E value){
        // fill your code
        maxHeap.insert(value);
        maxHeap.printHeap();
    }

    public void remove(E value){
        // fill your code
        maxHeap.remove(maxHeap.find(value));
        maxHeap.printHeap();
    }

    public void sort(int order){
        // fill your code
        E[] copyed = newArray(n);
        int heapsize = maxHeap.heapsize();
        if(order == SORT_A) {    //ascending
            for(int i = heapsize-1; i >= 0; i--) {
                copyed[i] = maxHeap.removeMax();
            }
        } else {            //descending
            for(int i = 0; i < heapsize; i++) {
                copyed[i] = maxHeap.removeMax();
            }
        }
        for(int i = 0; i < heapsize; i++) {
            System.out.print(copyed[i] + " ");
        }
        System.out.println();
        maxHeap.setSize(heapsize);
        maxHeap.buildheap();
        System.out.print("\t\t");
        maxHeap.printHeap();
    }

    public void sortLargest(int k) {
        // fill your code
        E[] copyed = newArray(n);
        int heapsize = maxHeap.heapsize();
        for(int i = 0; i < k; i++) {
            copyed[i] = maxHeap.removeMax();
        }
        for(int i = 0; i < k; i++) {
            System.out.print(copyed[i] + " ");
        }
        System.out.println();
        maxHeap.setSize(heapsize);
        maxHeap.buildheap();
        System.out.print("\t\t");
        maxHeap.printHeap();
    }

    //This function is for allocating an generic array of size n
    private static <E> E[] newArray(int length, E... array)
    {
        return Arrays.copyOf(array, length);
    }
}
