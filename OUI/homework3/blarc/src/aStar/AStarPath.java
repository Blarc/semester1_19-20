package aStar;

import core.api.commands.Direction;

import java.util.PriorityQueue;
import java.util.Stack;

public class AStarPath {

    private Node[][] nodes;

    private Node start;
    private Node end;

    private PriorityQueue<Node> openNodes;

    public AStarPath(AStar aStar) {
        aStar.reset();
        this.nodes = aStar.getNodes();
        this.openNodes = new PriorityQueue<>();
    }

    public void setStart(int x, int y) {
        this.start = nodes[y][x];
        openNodes.add(start);
    }

    public void setEnd(int x, int y) {
        this.end = nodes[y][x];
    }

    public Stack<Direction> findPath() {

        while(!openNodes.isEmpty()) {
            Node current = openNodes.poll();
            current.setClosed();

            if (current.equals(end)) {
                return getPath(current);
            } else {
                checkNeighbours(current);
            }
        }

        return new Stack<>();
    }

    private void checkNeighbours(Node current) {
        current.getNeighbours().forEach(node -> {
            if (!node.isClosed() && (node.getParent() == null ||
                    node.getParent().getGCost() > current.getGCost())) {
                node.setParent(current);
                node.setGCost(current.cost(node) + current.getGCost());
                node.setHCost(node.cost(end));
                openNodes.add(node);
            }
        });
    }

    private Stack<Direction> getPath(Node currentNode) {
        Stack<Direction> path = new Stack<>();
        Node parent;
        while ((parent = currentNode.getParent()) != null) {
            if (parent.x < currentNode.x) {
                path.push(Direction.RIGHT);
            }
            if (parent.x > currentNode.x) {
                path.push(Direction.LEFT);
            }
            if (parent.y < currentNode.y) {
                path.push(Direction.UP);
            }
            if (parent.y > currentNode.y) {
                path.push(Direction.DOWN);
            }
            currentNode = parent;
        }

        return path;
    }

}
