package aStar;

import core.api.Coin;
import core.api.Unit;
import core.api.commands.Direction;

import java.util.PriorityQueue;
import java.util.Stack;

public class AStarPath {

    private Node end;

    private PriorityQueue<Node> openNodes;

    public AStarPath(AStar aStar, Point unit, Point coin) {
        aStar.reset();
        this.openNodes = new PriorityQueue<>();
        openNodes.add(aStar.getNode(unit));
        this.end = aStar.getNode(coin);
    }

    public Stack<Point> findPath() {

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

    private Stack<Point> getPath(Node currentNode) {
        Stack<Point> path = new Stack<>();
        Node parent;
        while ((parent = currentNode.getParent()) != null) {
            path.push(new Point(currentNode.x, currentNode.y));
            currentNode = parent;
        }

        return path;
    }

}
