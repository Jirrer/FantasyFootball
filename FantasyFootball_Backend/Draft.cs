namespace FantasyFootball;

using System;
using System.ComponentModel.DataAnnotations;

public class Draft
{
    public Dictionary<int, Player> players = new Dictionary<int, Player>();
    private Team[] teams;

    private void populatePlayers()
    {
        // use database here

        players.Add(1, new Player("Ja'Marr Chase", "CIN", "WR", 1, 335.39));
        players.Add(2, new Player("Justin Jefferson", "MIN", "WR", 2, 320.45));
        players.Add(3, new Player("Cooper Kupp", "LAR", "WR", 3, 310.22));
        players.Add(4, new Player("Josh Allen", "BUF", "QB", 4, 298.15));
        players.Add(5, new Player("Derrick Henry", "TEN", "RB", 5, 287.50));
        players.Add(6, new Player("Travis Kelce", "KC", "TE", 6, 275.80));
        players.Add(7, new Player("Jonathan Taylor", "IND", "RB", 7, 260.10));
        players.Add(8, new Player("Davante Adams", "LV", "WR", 8, 255.75));
        players.Add(9, new Player("Patrick Mahomes", "KC", "QB", 9, 250.00));
        players.Add(10, new Player("Nick Chubb", "CLE", "RB", 10, 245.60));
        players.Add(11, new Player("Stefon Diggs", "BUF", "WR", 11, 240.50));
        players.Add(12, new Player("Dalvin Cook", "MIN", "RB", 12, 235.75));
        players.Add(13, new Player("George Kittle", "SF", "TE", 13, 220.30));
        players.Add(14, new Player("Lamar Jackson", "BAL", "QB", 14, 215.80));
        players.Add(15, new Player("Alvin Kamara", "NO", "RB", 15, 210.10));
        players.Add(16, new Player("DK Metcalf", "SEA", "WR", 16, 205.40));
        players.Add(17, new Player("Mark Andrews", "BAL", "TE", 17, 200.90));
        players.Add(18, new Player("Justin Herbert", "LAC", "QB", 18, 195.60));
        players.Add(19, new Player("Aaron Jones", "GB", "RB", 19, 190.25));
        players.Add(20, new Player("Mike Evans", "TB", "WR", 20, 185.80));

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
        foreach (var n in players)
        {
            Console.WriteLine($"{n.Key}: {n.Value.name} {n.Value.team}");
        }



        Console.Write($"{team.name}'s pick: ");
        string? input = Console.ReadLine();
        int playerId;
        if (!int.TryParse(input, out playerId))
        {
            Console.WriteLine("Invalid input. Please enter a valid number.");
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