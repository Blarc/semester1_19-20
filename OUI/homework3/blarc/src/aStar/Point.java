package aStar;

import core.api.Coin;
import core.api.Saw;
import core.api.Unit;
import core.api.commands.Direction;

import java.util.Objects;

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

    public Direction getDirection(Point point) {

        if (this.x < point.x) {
            return Direction.RIGHT;
        }
        if (this.x > point.x) {
            return Direction.LEFT;
        }
        if (this.y < point.y) {
            return Direction.UP;
        }
        return Direction.DOWN;
    }

    public Point translate(Direction direction) {

        if (direction == Direction.DOWN) {
            return new Point(this.x, this.y - 1);
        }
        if (direction == Direction.UP) {
            return new Point(this.x, this.y + 1);
        }
        if (direction == Direction.LEFT) {
            return new Point(this.x - 1, this.y);
        }
        return new Point(this.x + 1, this.y);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Point point = (Point) o;
        return x == point.x &&
                y == point.y;
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }
}
