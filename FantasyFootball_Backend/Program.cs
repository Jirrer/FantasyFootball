namespace FantasyFootball;

using System;

static class Program
{
    static void Main()
    {
        Team[] teams =
        [
            new Team("Team 1"),
            new Team("Team 2"),
            new Team("Team 3"),
            new Team("Team 4"),
            new Team("Team 5"),
            new Team("Team 6"),
            new Team("Team 7"),
            new Team("Team 8"),
            new Team("Team 9"),
            new Team("Team 10"),
            new Team("Team 11"),
            new Team("Team 12"),
        ];

        Draft draft = new Draft(teams);

        draft.run();
    }
}
