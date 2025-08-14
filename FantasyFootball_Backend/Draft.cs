namespace FantasyFootball;

using System;
using System.Data.SQLite;

public class Draft
{
    private readonly Team[] teams;
    public Dictionary<int, Player> players = new Dictionary<int, Player>();
    private Dictionary<string, List<Player>> playersByTeam = new Dictionary<string, List<Player>>();
    HashSet<Player> seenPlayers = new HashSet<Player>();

    public Draft(Team[] teams)
    {
        this.teams = teams;
        populatePlayers();
        orderTeams();
    }

    private void populatePlayers()
    {
        string connectionString = "Data Source=FantasyFootball.db;Version=3";

        using var connection = new SQLiteConnection(connectionString);
        connection.Open();

        string query = "SELECT name, team, position FROM players order by team, position;";

        using var command = new SQLiteCommand(query, connection);
        using SQLiteDataReader reader = command.ExecuteReader();

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

    private void orderTeams()
    {
        foreach (var player in players)
        {
            if (!string.IsNullOrEmpty(player.Value.team))
            {
                if (playersByTeam.ContainsKey(player.Value.team)) { playersByTeam[player.Value.team].Add(player.Value); }
                else { playersByTeam[player.Value.team] = new List<Player> { player.Value }; }
            }
        }
    }

    public void run()
    {
        for (int roundNumber = 1; roundNumber <= 15; roundNumber++)
        {
            int index = 0;
            while (index < teams.Length)
            {
                try
                {
                    Team playerUp = teams[index];
                    if (getPick(playerUp)) { Console.WriteLine("Player Added"); index++; }
                    else { Console.WriteLine("Invalid pick"); }
                }
                catch (KeyNotFoundException)
                {
                    Console.WriteLine("Invalid pick");
                }
            }

            Array.Reverse(teams);
        }
    }

    private bool getPick(Team team)
    {
        printTeams();

        Console.WriteLine($"\n{team.numWR}/3 WR | {team.numRB}/3 RB | {team.numQB}/3 QB | {team.numTE}/2 TE | {team.numK}/2 K | {team.numDFS}/2 DFS");
        Console.Write($"{team.name}'s pick: ");

        string? input = Console.ReadLine();

        if (!int.TryParse(input, out int playerId)) { return false; }

        bool addedPlayer;
        switch (players[playerId].position)
        {
            case "WR":
                if (team.numWR < 3) { team.addPlayer(players[playerId]); addedPlayer = true; break; }
                else { return false; }

            case "RB":
                if (team.numRB < 3) { team.addPlayer(players[playerId]); addedPlayer = true; break; }
                else { return false; }

            case "QB":
                if (team.numQB < 3) { team.addPlayer(players[playerId]); addedPlayer = true; break; }
                else { return false; }

            case "TE":
                if (team.numTE < 2) { team.addPlayer(players[playerId]); addedPlayer = true; break; }
                else { return false; }

            case "K":
                if (team.numK < 2) { team.addPlayer(players[playerId]); addedPlayer = true; break; }
                else { return false; }

            case "DFS":
                if (team.numDFS < 2) { team.addPlayer(players[playerId]); addedPlayer = true; break; }
                else { return false; }

            default:
                Console.WriteLine("error in finidng position");
                return false;
        }

        if (addedPlayer)
        {
            if (seenPlayers.Contains(players[playerId])) { players.Remove(playerId); }
            else { seenPlayers.Add(players[playerId]); }
        }

        return addedPlayer;
    }

    private void printTeams()
    {
        foreach (var teamsPlayers in playersByTeam)
        {
            Console.WriteLine($"\n{teamsPlayers.Key}"); 

            foreach (var player in teamsPlayers.Value)
            {
                var match = players.FirstOrDefault(p => p.Value == player);
                if (!match.Equals(default(KeyValuePair<int, Player>))) { Console.WriteLine($"{match.Key}: {player.name} | {player.position} | {player.team}"); }
                else { Console.WriteLine($"N/A: {player.name} | {player.position} | {player.team}"); }
            }
        }
    }

    public void showDraftResult()
    {
        foreach (Team team in teams)
        {
            Dictionary<string, List<Player>> teamsPlayers = new Dictionary<string, List<Player>>
            {
                {"QB", new List<Player>()},
                {"WR", new List<Player>()},
                {"RB", new List<Player>()},
                {"TE", new List<Player>()},
                {"K", new List<Player>()},
                {"DFS", new List<Player>()}
            };

            foreach (Player player in team.players)
            {
                if (!string.IsNullOrEmpty(player.position) && teamsPlayers.ContainsKey(player.position)) { teamsPlayers[player.position].Add(player); }
            }

            Console.WriteLine($"\nTeam - {team.name}");
            Console.Write($"QBs"); foreach (var x in teamsPlayers["QB"]) { Console.Write($" | {x.name} - {x.team}"); }
            Console.Write($"\nWR"); foreach (var x in teamsPlayers["WR"]) { Console.Write($" | {x.name} - {x.team}"); }
            Console.Write($"\nRB"); foreach (var x in teamsPlayers["RB"]) { Console.Write($" | {x.name} - {x.team}"); }
            Console.Write($"\nTE"); foreach (var x in teamsPlayers["TE"]) { Console.Write($" | {x.name} - {x.team}"); }
            Console.Write($"\nK"); foreach (var x in teamsPlayers["K"]) { Console.Write($" | {x.name} - {x.team}"); }
            Console.Write($"\nDFS"); foreach (var x in teamsPlayers["DFS"]) { Console.Write($" | {x.name} - {x.team}"); }
        }
    }
}