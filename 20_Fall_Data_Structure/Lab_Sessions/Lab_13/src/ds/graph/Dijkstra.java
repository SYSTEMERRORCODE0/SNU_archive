package ds.graph;

import ds.queue.DistanceQueue;

public class Dijkstra {
    private DistanceQueue distQueue;
    private int[] prev;
    private double[] D;
    private Graph G;

    public Dijkstra(Graph G) {
        // Fill your code
    	D = new double[G.n()];
    	distQueue = new DistanceQueue(G.n());
    	prev = new int[G.n()];
    	this.G= G;
    }

    public void calculateShortestPath(Graph G, int start) {
        // Fill your code here
        int n = G.n();
        for(int i = 0; i < n; i++) {
            D[i] = Integer.MAX_VALUE;
            prev[i] = -1;
            distQueue.insert(i, D[i]);
        }
        D[start] = 0;
        distQueue.decreaseDistance(start, 0);
        for(int i = 0; i < n; i++) {
            int a = minVertex(G);
            for(int b = G.first(a); b < n; b = G.next(a, b)) {
                if(D[a] + G.weight(a, b) < D[b]) {
                    D[b] = D[a] + G.weight(a, b);
                    distQueue.decreaseDistance(b, D[b]);
                    prev[b] = a;
                }
            }
        }
    }
	public void delNode(Graph G, int v) {
		// Fill your code here
        int n = G.n();
        for(int i = 0; i < n; i++) {
            G.delEdge(v, i);
        }
        for(int i = 0; i < n; i++) {
            G.delEdge(i, v);
        }
	}

    public void printPathToEnd(Graph G, int end) {
        // Fill your code here
        int vertex = end;
        String string = Integer.toString(vertex);
        while(prev[vertex] != -1) {
            vertex = prev[vertex];
            string = vertex + " " + string;
        }
        System.out.println(string);
    }
    
    public void printAllPath(Graph G, int src) {
		// Fill your code here
        int n = G.n();
        for(int i = 0; i < n; i++) {
            if(D[i] == (double)Integer.MAX_VALUE) {
                System.out.print("PATH " + src + " " + i + ": INF ");
            } else {
                System.out.print("PATH " + src + " " + i + ": " + D[i] + " ");
            }
            printPathToEnd(G, i);
        }
    }

    public int minVertex(Graph G) {
    	return distQueue.removeMin();
    }

}
