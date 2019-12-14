package aStar;

import java.util.List;

public class Node implements Comparable<Node> {

    /*
    gCost = distance from starting node
    hCost = distance from end node
    fCost = gCost + fCost
    */

    public int x;
    public int y;

    private int gCost;
    private int hCost;

    private NodeType type;
    private Node parent;
    private List<Node> neighbours;

    public Node(int x, int y) {
        this.x = x;
        this.y = y;
        this.type = NodeType.OPEN;
    }

    public void reset() {
        this.type = NodeType.OPEN;
        this.parent = null;
        this.gCost = 0;
        this.hCost = 0;
    }

    public Node getParent() {
        return parent;
    }

    public void setParent(Node parent) {
        this.parent = parent;
    }

    public List<Node> getNeighbours() {
        return neighbours;
    }

    public void setNeighbours(List<Node> neighbours) {
        this.neighbours = neighbours;
    }

    public int getGCost() {
        return gCost;
    }

    public void setGCost(int gCost) {
        this.gCost = gCost;
    }

    public void setHCost(int hCost) {
        this.hCost = hCost;
    }

    public int getFCost() {
        return this.gCost + this.hCost;
    }

    public void setClosed() {
        this.type = NodeType.CLOSED;
    }

    public boolean isClosed() {
        return this.type == NodeType.CLOSED;
    }

    // Manhattan distance
    public int cost(Node node) {
        return abs(this.x - node.x) + abs(this.y - node.y);
    }

    private int abs(int a) {
        return a > 0 ? a : -a;
    }

    @Override
    public int compareTo(Node node) {
        return this.getFCost() - node.getFCost();
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Node node = (Node) o;
        return x == node.x &&
                y == node.y;
    }
}
