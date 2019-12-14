package core.api;

import aStar.Point;

public class Coin {
    public int x;
    public int y;

    public Coin(int x, int y) {
        this.x = x;
        this.y = y;
    }

    public Coin(Point point) {
        this.x = point.x;
        this.y = point.y;
    }
}
