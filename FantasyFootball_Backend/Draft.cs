namespace FantasyFootball;

using System;
using System.Data.SQLite;

public class Draft
{
    public Dictionary<int, Player> players = new Dictionary<int, Player>();
    private Team[] teams;

    private void populatePlayers()
    {
        string connectionString = "Data Source=FantasyFootball.db;Version=3";

        using (var connection = new SQLiteConnection(connectionString))
        {
            connection.Open();

            string query = "SELECT id, name, team, position, jersey, projection FROM players";

            using (var command = new SQLiteCommand(query, connection))
            {
                using (SQLiteDataReader reader = command.ExecuteReader())
                {
                    while (reader.Read())
                    {
                        players.Add(
                            reader.GetInt32(0),
                            new Player(reader.GetString(1),
                            reader.GetString(2),
                            reader.GetString(3),
                            reader.GetInt32(4),
                            reader.GetDouble(5)
                        ));
                    }
                }
            }
        }
    }

    public Draft(Team[] teams)
    {
        this.teams = teams;
        populatePlayers();

    }

    public void run()
    {
        int roundNumber = 1;
        while (roundNumber <= 15)
        {
            int index = 0;
            while (index < teams.Length)
            {
                Team playerUp = teams[index];
                if (getPick(playerUp)) { Console.WriteLine("Player Added"); index++; }
                else { Console.WriteLine("Invalid pick"); }
            }

            Array.Reverse(teams);
            roundNumber++;
        }
    }

    private bool getPick(Team team)
    {
        foreach (var n in players.Reverse()) { Console.WriteLine($"{n.Key}: {n.Value.name} | {n.Value.position} | {n.Value.team} | {n.Value.projection}"); }

        Console.WriteLine($"\n{team.numWR}/3 WR | {team.numRB}/3 RB | {team.numQB}/3 QB | {team.numTE}/2 TE | {team.numK}/2 K | {team.numDFS}/2 DFS");
        Console.Write($"{team.name}'s pick: ");
        string? input = Console.ReadLine();
        int playerId;
        if (!int.TryParse(input, out playerId))
        {
            return false;
        }

        switch (players[playerId].position)
        {
            case "WR":
                if (team.numWR < 3) { team.addPlayer(players[playerId]); players.Remove(playerId); return true; }
                else { return false; }

            case "RB":
                if (team.numRB < 3) { team.addPlayer(players[playerId]); players.Remove(playerId); return true; }
                else { return false; }

            case "QB":
                if (team.numQB < 3) { team.addPlayer(players[playerId]); players.Remove(playerId); return true; }
                else { return false; }

            case "TE":
                if (team.numTE < 2) { team.addPlayer(players[playerId]); players.Remove(playerId); return true; }
                else { return false; }

            case "K":
                if (team.numK < 2) { team.addPlayer(players[playerId]); players.Remove(playerId); return true; }
                else { return false; }

            case "DFS":
                if (team.numDFS < 2) { team.addPlayer(players[playerId]); players.Remove(playerId); return true; }
                else { return false; }

            default:
                Console.WriteLine("error in finidng position");
                return false;
        }
    }
}