
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    private static final int TABLE_SIZE = 11;
    private static final int ERROR = -1;
    private static final int INSERT = 1;
    private static final int DELETE = 2;
    private static final int SEARCH = 3;

    public static void main(String[] args) throws IOException {
        HashTable hashTable = new HashTable(TABLE_SIZE);
        String filePath;

        try {
            filePath = args[0];
        } catch (ArrayIndexOutOfBoundsException e) {
            filePath = "sample_input.txt";
        }

        FileInputStream fis = new FileInputStream(filePath);
        BufferedReader reader = new BufferedReader(new InputStreamReader(fis));

        for (String line = reader.readLine(); line != null; line = reader.readLine()) {
            String[] lineSplit = line.split(" ");
            String cmd = lineSplit[0];

            int key;

            switch (getCommandNum(cmd)) {
                case INSERT:
                    key = Integer.parseInt(lineSplit[1]);
                    hashTable.insert(key);
                    break;
                case DELETE:
                    key = Integer.parseInt(lineSplit[1]);
                    hashTable.delete(key);
                    break;
                case SEARCH:
                    key = Integer.parseInt(lineSplit[1]);
                    hashTable.search(key);
                    break;
            }
        }
        reader.close();
    }

    private static int getCommandNum(String cmd) {
        switch (cmd) {
            case "insert":
                return INSERT;
            case "delete":
                return DELETE;
            case "search":
                return SEARCH;
            default:
                return ERROR;
        }
    }

}
