import ds.graph.Dijkstra;
import ds.graph.Graph;
import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.InputStreamReader;
import java.util.LinkedList;

public class Main {

    @SuppressWarnings("resource")
    public static void main(String[] args) {
        FileInputStream fis = null;
        BufferedReader reader = null;
        Graph G = null;

        try {
            fis = new FileInputStream("sample_input.txt");
        } catch (FileNotFoundException e) {
            e.printStackTrace();
            return;
        }
        reader = new BufferedReader(new InputStreamReader(fis));

        String line;

        try {
            for (line=reader.readLine(); line !=null; line=reader.readLine()) {
                String[] line_split = line.split(" ");
                String cmd_type = line_split[0];

                if (cmd_type.equals("init")) {
                    String cmd = line_split[1];
                    int n = Integer.valueOf(line_split[1]);
                    G = new Graph(n);
                } else if (cmd_type.equals("setedge")) {
                    int src = Integer.valueOf(line_split[1]);
                    int dst = Integer.valueOf(line_split[2]);
                    double w = Double.valueOf(line_split[3]);
                    G.setEdge(src, dst, w);
                } else if (cmd_type.equals(("deledge"))) {
                    int src = Integer.valueOf(line_split[1]);
                    int dst = Integer.valueOf(line_split[2]);
                    G.delEdge(src, dst);
                } else if (cmd_type.equals("delnode")) {
                    int src = Integer.valueOf(line_split[1]);
                    Dijkstra dijkstra = new Dijkstra(G);
                    dijkstra.delNode(G, src);
                } else if (cmd_type.equals("shortestpath")) {
                    int src = Integer.valueOf(line_split[1]);
                    Dijkstra dijkstra = new Dijkstra(G);
                    dijkstra.calculateShortestPath(G, src);
                    dijkstra.printAllPath(G, src);
                }
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }


}