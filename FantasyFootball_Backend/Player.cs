namespace FantasyFootball;

using System;

public class Player
{
    public string? name { get; }
    public string? team { get; }
    public string? position { get; }

    public Player(string name, string team, string position)
    {
        this.name = name;
        this.team = team;
        this.position = position;
    }
}
