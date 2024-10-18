import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;

public class Main {
    public static void main(String[] args) throws Exception {
        SortManager manager = new SortManager();
        FileInputStream fis = new FileInputStream("sample_input.txt");
        BufferedReader reader = new BufferedReader(new InputStreamReader(fis));

        for (String line = reader.readLine(); line != null; line = reader.readLine()) {
            String[] cmd = line.split(" ");

            switch (cmd[0]) {
                case "SET_ITEMS":
                    int n = Integer.parseInt(cmd[1]);
                    String itemLine = reader.readLine();
                    manager.setItems(n, itemLine);
                    break;

                case "BUBBLE_SORT":
                    manager.doBubbleSort();
                    break;

                case "SELECTION_SORT":
                    manager.doSelectionSort();
                    break;

                case "STABLE_SELECTION_SORT":
                    manager.doStableSelectionSort();
                    break;

                case "CHECK":
                    manager.check();
                    break;
            }

        }
    }
}
