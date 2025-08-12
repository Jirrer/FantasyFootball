namespace FantasyFootball;

using System;

public class Player
{
    public string ?name { get; }
    public string ?team { get; }
    public string ?position{ get; } 
    public int number { get; }
    public float projection { get; }

    public Player(string name, string team, string position, int number, float projection) {}
}