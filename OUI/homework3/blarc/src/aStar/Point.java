package aStar;

import core.api.Coin;
import core.api.Saw;
import core.api.Unit;

public class Point {
    public int x;
    public int y;

    public Point(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public Point(Unit unit) {
        this.x = unit.x;
        this.y = unit.y;
    }

    public Point(Coin coin) {
        this.x = coin.x;
        this.y = coin.y;
    }

    public Point(Saw saw) {
        this.x = saw.x;
        this.y = saw.y;
    }

    public int manhattan(Point point) {
        return Utils.manhattan(this, point);
    }
}
