import aStar.AStar;
import aStar.AStarPath;
import com.google.gson.Gson;
import core.*;
import core.api.*;
import core.api.commands.Direction;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Stack;

/**
 * Example Java bot implementation for Planet Lia Bounce Evasion.
 */
public class MyBot implements Bot {

    private InitialData data;

    private AStar aStar;

    private Coin coin;

    private Stack<Direction> path;

    // Called only once before the match starts. It holds the
    // data that you may need before the game starts.
    @Override
    public void setup(InitialData data) {
        System.out.println((new Gson()).toJson(data));
        this.data = data;

        // Print out the map
        for (int y = data.mapHeight - 1; y >= 0; y--) {
            for (int x = 0; x < data.mapWidth; x++) {
                System.out.print((data.map[y][x]) ? "_" : "#");
            }
            System.out.println();
        }

        this.aStar = new AStar(data);
    }

    // Called repeatedly while the match is generating. Each
    // time you receive the current match state and can use
    // response object to issue your commands.
    @Override
    public void update(MatchState state, Response response) {
        // Find and send your unit to a random direction that
        // moves it to a valid field on the map
        // TODO: Remove this code and implement a proper path finding!

        Coin currentCoin = state.coins[0];
        if (coin == null && currentCoin != null) {
            coin = currentCoin;
            AStarPath aStarPath = new AStarPath(this.aStar);
            aStarPath.setStart(state.yourUnit.x, state.yourUnit.y);
            aStarPath.setEnd(state.coins[0].x, state.coins[0].y);
            path = aStarPath.findPath();
        }

        if (!path.empty()) {
            Direction dir = path.pop();
            System.out.println(dir.toString());
            response.moveUnit(dir);
        } else {
            coin = null;
        }

    }

    // Connects your bot to match generator, don't change it.
    public static void main(String[] args) throws Exception {
        NetworkingClient.connectNew(args, new MyBot());
    }
}
