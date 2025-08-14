namespace FantasyFootball;

using System;

public class Team
{
    public string name { get; }
    public List<Player> players = new List<Player>();
    public int numWR = 0;
    public int numRB = 0;
    public int numQB = 0;
    public int numTE = 0;
    public int numK = 0;
    public int numDFS = 0;

    public Team(string name) { this.name = name; }
    
    public void addPlayer(Player player)
    {

        players.Add(player);

        switch (player.position)
        {
            case "WR": numWR++; break;
            case "RB": numRB++; break;
            case "QB": numQB++; break;
            case "TE": numTE++; break;
            case "K": numK++; break;
            case "DFS": numDFS++; break;
            default: Console.WriteLine("Error adding player"); break;
        }
    }
}