import aStar.*;
import com.google.gson.Gson;
import core.*;
import core.api.*;
import core.api.commands.Direction;


import java.util.Arrays;
import java.util.Comparator;
import java.util.Stack;

/**
 * Example Java bot implementation for Planet Lia Bounce Evasion.
 */
public class MyBot implements Bot {

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
            long startTime = System.currentTimeMillis();

            path = new AStarPath(this.aStar, unit, coin).findPath();

            long endTime = System.currentTimeMillis();
            System.out.println("Time: " + (endTime - startTime) + " ms");
        }


        Point point = path.pop();

        Direction dir = Utils.getDirection(unit, point);

        response.moveUnit(dir);

    }

    private Point getClosestCoin(Point unit, Coin[] coins) {
        // FIXME new Coin(unit.x, unit.y)
        return Arrays.stream(coins)
                .map(c -> new Point(c))
                .min(Comparator.comparingInt(c -> c.manhattan(unit)))
                .orElse(unit);
    }

    // Connects your bot to match generator, don't change it.
    public static void main(String[] args) throws Exception {
        NetworkingClient.connectNew(args, new MyBot());
    }
}
