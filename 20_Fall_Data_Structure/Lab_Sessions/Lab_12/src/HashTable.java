
public class HashTable {
    private int[] table;
    private int delMarker = -1;
    private int tableSize;

    public HashTable(int n) {
        tableSize = n;
        table = new int[tableSize];
    }

    public void insert(int key) {
        //TODO: fill your code
        int h_key = key % tableSize;
        int index = h_key;
        for(int i = 1; table[index] > 0; i++) {
            index = (h_key + i) % tableSize;
        }
        table[index] = key;
        System.out.println("INSERT: " + key + ", INDEX: " + index);
    }

    public void delete(int key) {
        //TODO: fill your code
        int h_key = key % tableSize;
        int index = h_key;
        for(int i = 1; table[index] != key && table[index] != 0; i++) {
            index = (h_key + i) % tableSize;
        }
        if(table[index] == 0) {
            System.out.println("Failed to find " + key);
        } else {
            table[index] = delMarker;
            System.out.println("DELETE: " + key + ", INDEX: " + index);
        }
    }

    public void search(int key) {
        //TODO: fill your code
        int h_key = key % tableSize;
        int index = h_key;
        for(int i = 1; table[index] != key && table[index] != 0; i++) {
            index = (h_key + i) % tableSize;
        }
        if(table[index] == 0) {
            System.out.println("Failed to find " + key);
        } else {
            System.out.println("DELETE: " + key + ", INDEX: " + index);
            if(index != h_key) {
                int temp = table[index];
                table[index] = table[(index + tableSize - 1) % tableSize];
                table[(index + tableSize - 1) % tableSize] = temp;
            }
        }
    }

}
