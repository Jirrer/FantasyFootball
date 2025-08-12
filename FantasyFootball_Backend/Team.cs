namespace FantasyFootball;

using System;

public class Team
{
    public string? name { get; }
    private Player[] players = new Player[15];
    public int numWR = 0;
    public int numRB = 0;
    public int numQB = 0;
    public int numTE = 0;
    public int numK = 0;
    public int numDFS = 0;

    public Team(string name)
    {
        this.name = name;
    }
    public void addPlayer(Player player)
    {
        for (int index = 0; index < players.Length; index++)
        {
            if (players[index] == null) { players[index] = player; }
        }

    }
    






}