package aStar;

import core.api.InitialData;

import java.util.*;

public class AStar {

    private InitialData data;

    private Node[][] nodes;

    public AStar(InitialData data) {
        this.data = data;
        boolean[][] map = data.map;
        this.nodes = new Node[data.mapHeight][data.mapWidth];

        for (int y = 0; y < data.mapHeight; y++) {
            for (int x = 0; x < data.mapWidth; x++) {
                if (map[y][x]) {
                    nodes[y][x] = new Node(x, y);
                }
            }
        }

        for (int y = 0; y < data.mapHeight; y++) {
            for (int x = 0; x < data.mapWidth; x++) {
                if (map[y][x]) {
                    initNeighbours(nodes[y][x]);
                }
            }
        }
    }

    private void initNeighbours(Node node) {
        List<Node> neighbours = new ArrayList<>();
        if (node.x > 0) {
            Node tmp = nodes[node.y][node.x - 1];
            if (tmp != null) {
                neighbours.add(tmp);
            }
        }
        if (node.x < data.mapWidth - 1) {
            Node tmp = nodes[node.y][node.x + 1];
            if (tmp != null) {
                neighbours.add(tmp);
            }
        }
        if (node.y > 0) {
            Node tmp = nodes[node.y - 1][node.x];
            if (tmp != null) {
                neighbours.add(tmp);
            }
        }
        if (node.y < data.mapHeight - 1) {
            Node tmp = nodes[node.y + 1][node.x];
            if (tmp != null) {
                neighbours.add(tmp);
            }
        }

        node.setNeighbours(neighbours);
    }

    public Node getNode(Point point) {
        return nodes[point.y][point.x];
    }

    public boolean isValid(Point point) {
        if (point.x >= 0 && point.x < data.mapWidth && point.y >= 0 && point.y < data.mapHeight) {
            return nodes[point.y][point.x] != null;
        }
        return false;
    }

    public void reset() {
        for (int y = 0; y < data.mapHeight; y++) {
            for (int x = 0; x < data.mapWidth; x++) {
                Node tmp = nodes[y][x];
                if (tmp != null) {
                    tmp.reset();
                }
            }
        }
    }
}