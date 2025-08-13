namespace FantasyFootball;

using System;
using System.Data.SQLite;

public class Draft
{
    public Dictionary<int, Player> players = new Dictionary<int, Player>();
    private Dictionary<string, List<Player>> playersByTeam = new Dictionary<string, List<Player>>();
    private Team[] teams;

    private void populatePlayers()
    {
        string connectionString = "Data Source=FantasyFootball.db;Version=3";

        using (var connection = new SQLiteConnection(connectionString))
        {
            connection.Open();

            string query = "SELECT name, team, position FROM players";

            using (var command = new SQLiteCommand(query, connection))
            {
                using (SQLiteDataReader reader = command.ExecuteReader())
                {
                    int id = 1;
                    while (reader.Read())
                    {
                        players.Add(
                            id,
                            new Player(
                                reader.GetString(0),
                                reader.GetString(1),
                                reader.GetString(2)
                            ));

                        id++;
                    }
                }
            }
        }
    }

    private void orderTeams()
    {
        foreach (var player in this.players)
        {
            #pragma warning disable CS8604
            if (playersByTeam.ContainsKey(player.Value.team)) { playersByTeam[player.Value.team].Add(player.Value); }
            else { playersByTeam[player.Value.team] = new List<Player> { player.Value }; }
        }
    }

    public Draft(Team[] teams)
    {
        this.teams = teams;
        populatePlayers();
        orderTeams();

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
        printTeams();

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

    private void printTeams()
    {
        foreach (var kvp in playersByTeam)
        {
            Console.WriteLine($"\n{kvp.Key}"); // Team name
            foreach (var player in kvp.Value)
            {
                var match = players.FirstOrDefault(p => p.Value == player);
                if (!match.Equals(default(KeyValuePair<int, Player>)))
                {
                    Console.WriteLine($"{match.Key}: {player.name} | {player.position} | {player.team}");
                }
                else
                {
                    // Print alternative key if not found
                    Console.WriteLine($"N/A: {player.name} | {player.position} | {player.team}");
                }
            }
        }
    }
}