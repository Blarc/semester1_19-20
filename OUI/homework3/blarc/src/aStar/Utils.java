package aStar;

import core.api.Unit;
import core.api.commands.Direction;

public class Utils {

    public static int manhattan(Point a, Point b) {
        return abs(a.x - b.x) + abs(a.y - b.y);
    }

    public static int manhattan(int x1, int y1, int x2, int y2) {
        return abs(x1 - x2) + abs(y1 - y2);
    }

    public static int abs(int x) {
        return x > 0 ? x : -x;
    }

    public static Direction getDirection(Point unit, Point point) {

        if (unit.x < point.x) {
            return Direction.RIGHT;
        }
        if (unit.x > point.x) {
            return Direction.LEFT;
        }
        if (unit.y < point.y) {
            return Direction.UP;
        }
        return Direction.DOWN;
    }
}
