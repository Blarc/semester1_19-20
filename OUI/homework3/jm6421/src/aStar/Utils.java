package aStar;

import core.api.Saw;
import core.api.SawDirection;
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

    public static Point getNextSawPoint(Saw saw) {
        Point point = new Point(saw.x, saw.y);
        if (saw.direction == SawDirection.UP_LEFT) {
            point.x -= 1;
            point.y += 1;
        }
        else if (saw.direction == SawDirection.UP_RIGHT) {
            point.x += 1;
            point.y += 1;
        }
        else if (saw.direction == SawDirection.DOWN_LEFT) {
            point.x -= 1;
            point.y -= 1;
        }
        else {
            point.x += 1;
            point.y -= 1;
        }
        return point;
    }
}
