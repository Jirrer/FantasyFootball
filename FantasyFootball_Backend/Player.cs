namespace FantasyFootball;

using System;

public class Player
{
    public string? name { get; }
    public string? team { get; }
    public string? position { get; }
    public int number { get; }
    public double projection { get; }

    public Player(string name, string team, string position, int number, double projection)
    {
        this.name = name;
        this.team = team;
        this.position = position;
        this.number = number;
        this.projection = projection;
    }
}
