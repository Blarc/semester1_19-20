package core.api.commands;

public enum Direction {
    LEFT, RIGHT, UP, DOWN;

    public Direction getInverse() {
        if (this == LEFT) {
            return RIGHT;
        }
        if (this == RIGHT) {
            return LEFT;
        }
        if (this == UP) {
            return DOWN;
        }
        return UP;
    }
}
