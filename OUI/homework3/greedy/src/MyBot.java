import core.*;
import core.api.*;
import core.api.commands.Direction;

import java.util.*;
import java.util.stream.Collectors;


public class MyBot implements Bot {

    private static final int SAW_DISTANCE = 10;

    private boolean[][] map;

    private Stack<Direction> path;

    private Point unit;

    private Point coin;

    private Saw[] saws;

    private List<Point> visited;

    @Override
    public void setup(InitialData data) {
        this.map = data.map;
        this.unit = new Point(data.yourUnit);
        this.coin = getClosestCoin(data.coins);
        this.saws = data.saws;
        this.visited = new LinkedList<>();
    }

    @Override
    public void update(MatchState state, Response response) {

        unit = new Point(state.yourUnit);

        if (unit.equals(coin)) {
            this.visited = new LinkedList<>();
            coin = getClosestCoin(state.coins);
        }
        saws = state.saws;

        Point next = getNextPoint();
        if (next != null) {
            visited.add(next);
            response.moveUnit(unit.getDirection(next));
        }
    }

    private Point getNextPoint() {
        return Arrays.stream(Direction.values())
                .map(dir-> unit.translate(dir))
                .filter(point -> 0 <= point.y && point.y < map.length &&
                        0 <= point.x && point.x < map[0].length &&
                        map[point.y][point.x] &&
                        !visited.contains(point) &&
                        !sawCheck(point, getCloseSaws()))
                .min(Comparator.comparingInt(c -> c.manhattan(coin)))
                .orElse(null);
    }

    private Point getClosestCoin(Coin[] coins) {
        return Arrays.stream(coins)
                .map(Point::new)
                .min(Comparator.comparingInt(c -> c.manhattan(unit)))
                .orElse(unit);
    }

    private boolean sawCheck(Point point, List<Saw> saws) {
        return saws.stream()
                .anyMatch(saw -> Utils.getNextSawPoint(saw).equals(point));
    }

    private List<Saw> getCloseSaws() {
        return Arrays.stream(saws)
                .filter(saw -> unit.manhattan(new Point(saw.x, saw.y)) < SAW_DISTANCE)
                .collect(Collectors.toList());
    }

    // Connects your bot to match generator, don't change it.
    public static void main(String[] args) throws Exception {
        NetworkingClient.connectNew(args, new MyBot());
    }
}
