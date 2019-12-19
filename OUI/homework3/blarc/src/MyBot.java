import aStar.*;
import com.google.gson.Gson;
import core.*;
import core.api.*;
import core.api.commands.Direction;


import java.util.Arrays;
import java.util.Comparator;
import java.util.List;
import java.util.Stack;
import java.util.stream.Collectors;

/**
 * Example Java bot implementation for Planet Lia Bounce Evasion.
 */
public class MyBot implements Bot {

    private static final int SAW_DISTANCE = 4;

    private AStar aStar;

    private Point unit;

    private Point coin;

    private Stack<Point> path;

    // Called only once before the match starts. It holds the
    // data that you may need before the game starts.
    @Override
    public void setup(InitialData data) {
        this.aStar = new AStar(data);
        this.unit = new Point(data.yourUnit);
        this.coin = getClosestCoin(unit, data.coins);
        this.path = new AStarPath(aStar, unit, coin).findPath();
    }

    // Called repeatedly while the match is generating. Each
    // time you receive the current match state and can use
    // response object to issue your commands.
    @Override
    public void update(MatchState state, Response response) {

        unit = new Point(state.yourUnit);
        coin = getClosestCoin(unit, state.coins);

        if (path.empty()) {
            path = new AStarPath(this.aStar, unit, coin).findPath();
        }

        Point nextPoint = path.peek();
        List<Saw> closeSaws = getCloseSaws(nextPoint, state.saws);
        if (sawCheck(nextPoint, getCloseSaws(nextPoint, state.saws))) {
            Direction newDir = Arrays.stream(Direction.values())
                    .filter(dir -> {
                        Point tmp = nextPoint.translate(dir);
                        return aStar.isValid(tmp) && sawCheck(tmp, closeSaws);
                    })
                    .findFirst()
                    .orElse(null);
            if (newDir == null) {
                return;
            }
            else {
                path.push(nextPoint.translate(newDir));
                path.push(nextPoint.translate(newDir.getInverse()));
            }
        }


        response.moveUnit(unit.getDirection(path.pop()));

    }

    private Point getClosestCoin(Point unit, Coin[] coins) {
        // FIXME new Coin(unit.x, unit.y)
        return Arrays.stream(coins)
                .map(c -> new Point(c))
                .min(Comparator.comparingInt(c -> c.manhattan(unit)))
                .orElse(unit);
    }

    private boolean sawCheck(Point point, List<Saw> saws) {
        return saws.stream()
                .anyMatch(saw -> Utils.getNextSawPoint(saw).equals(point));
    }

    private List<Saw> getCloseSaws(Point point, Saw[] saws) {
        return Arrays.stream(saws)
                .filter(saw -> point.manhattan(new Point(saw.x, saw.y)) < SAW_DISTANCE)
                .collect(Collectors.toList());
    }

    // Connects your bot to match generator, don't change it.
    public static void main(String[] args) throws Exception {
        NetworkingClient.connectNew(args, new MyBot());
    }
}
