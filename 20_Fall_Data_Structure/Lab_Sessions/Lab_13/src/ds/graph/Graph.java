package ds.graph;

import ds.list.LinkedList;

import java.lang.reflect.Array;

public class Graph {
    private LinkedList<Edge>[] vertex;            // The vertex list
    private int numEdge;                   // Number of edges

    public Graph(int n) {
        init(n);
    }

    public void init(int n) {
        vertex = (LinkedList<Edge>[]) Array.newInstance(LinkedList.class, n);
        for (int i = 0; i < n; i++)
            vertex[i] = new LinkedList<Edge>();
        numEdge = 0;
    }

    public int n() {
        return vertex.length;
    }

    public int e() {
        return numEdge;
    }



    /**
     * @return v's first neighbor
     */
    public int first(int v) {
        if (vertex[v].length() == 0)
            return vertex.length;   // No neighbor
        vertex[v].moveToStart();
        Edge it = vertex[v].getValue();
        return it.vertex();
    }

    /**
     * @return v's next neighbor after w
     */
    public int next(int v, int w) {
        Edge it = null;
        if (isEdge(v, w)) {
            vertex[v].next();
            it = vertex[v].getValue();
        }
        if (it != null)
            return it.vertex();
        return vertex.length; // No neighbor
    }

    /**
     * Set the weight for an edge
     */
    public void setEdge(int i, int j, double weight) {
        Edge currEdge = new Edge(j, weight);

        if (!checkWeightValue(currEdge)){
            System.out.println("The weight must be positive.");
            return;
        }
        // Fill your code here
        if(isEdge(i, j)) {
            delEdge(i, j);
            vertex[i].insert(currEdge);
        } else {
            vertex[i].moveToStart();
            while(vertex[i].getValue() != null && vertex[i].getValue().vertex() < j) {
                vertex[i].next();
            }
            vertex[i].insert(currEdge);
        }
    }

    public boolean checkWeightValue(Edge testEdge) {
        if(testEdge.weight() <= 0) {
            return false;
        }
        return true;
    }


    /**
     * Delete an edge
     */
    public void delEdge(int i, int j) {
        // Fill your code here
        if(isEdge(i, j)) {
            vertex[i].remove();
            numEdge--;
        }
    }

    /**
     * Determine if an edge is in the graph
     */
    public boolean isEdge(int v, int w) {
        Edge it = vertex[v].getValue();
        // Check if j is the current neighbor in the list
        if ((it != null) && (it.vertex() == w)) {
            return true;
            }
        for (vertex[v].moveToStart();
             vertex[v].currPos() < vertex[v].length();
             vertex[v].next())              // Check whole list
            if (vertex[v].getValue().vertex() == w) return true;
        return false;
    }


    /**
     * @return an edge's weight
     */
    public double weight(int i, int j) {
        if (isEdge(i, j)) return vertex[i].getValue().weight();
        return 0;
    }
}
