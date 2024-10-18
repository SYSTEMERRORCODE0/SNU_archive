import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStreamReader;

public class Main {
    private static final int ERROR = -1;
    private static final int UNION = 0;
    private static final int GROUPSIZE = 1;
    private static final int DIFFER = 2;
    private static final int FIND = 3;
    private static final int DEPTH = 4;
    private static final int SUMMARY = 5;


    public static void main(String[] args) {
        try {
            int size = 10;
            ParPtrTree PPT = new ParPtrTree(size);
            FileInputStream fis = new FileInputStream("sample_input.txt");
            BufferedReader reader = new BufferedReader(new InputStreamReader(fis));

            for (String line = reader.readLine(); line != null; line = reader.readLine()) {
                String[] line_split = line.split(" ");
                String cmd = line_split[0];

                //PPT.print(); // use it for self-checking
                Integer Node1 = 0;
                Integer Node2 = 0;
                switch (getCommandNum(cmd)) {
                    case UNION:
                        Node1 = Integer.parseInt(line_split[1]);
                        Node2 = Integer.parseInt(line_split[2]);

                        // Print statement and call union function.
                        System.out.printf("Union %d and %d\n", Node1, Node2);
                        PPT.union(Node1, Node2);
                        break;

                    case GROUPSIZE:
                        Node1 = Integer.parseInt(line_split[1]);

                        // Call union function and print statement.
                        Integer s = PPT.groupSize(Node1);
                        System.out.println("GROUPSIZE: " + (s));
                        break;

                    case DIFFER:
                        Node1 = Integer.parseInt(line_split[1]);
                        Node2 = Integer.parseInt(line_split[2]);

                        // Call differ function and print statement.
                        boolean diff = PPT.differ(Node1, Node2);
                        if (diff) {
                            System.out.println("DIFFER: YES");
                        } else {
                            System.out.println("DIFFER: NO");
                        }
                        break;

                    case FIND:
                        Node1 = Integer.parseInt(line_split[1]);

                        //Call find function and print statement.
                        Integer root = PPT.find(Node1);
                        System.out.printf("%d's ROOT: %d\n", Node1, root);
                        break;

                    case DEPTH:
                        Node1 = Integer.parseInt(line_split[1]);
                        Integer depth = PPT.depth(Node1);
                        System.out.printf("%d's DEPTH: %d\n", Node1, depth);
                        break;

                    case SUMMARY:
                        PPT.summary();
                        break;

                    case ERROR:
                        System.out.println("ERROR: Unknown command");
                        break;
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private static int getCommandNum(String cmd) {
        //System.out.println(cmd);
        if (cmd.equals("union"))
            return UNION;
        else if (cmd.equals("groupsize"))
            return GROUPSIZE;
        else if (cmd.equals("differ"))
            return DIFFER;
        else if (cmd.equals("find"))
            return FIND;
        else if (cmd.equals("depth"))
            return DEPTH;
        else if (cmd.equals("summary"))
            return SUMMARY;
        else
            return ERROR;
    }
}

