namespace FantasyFootball;

using System;

static class Program
{
    private static Team[] teams =
        [
            new Team("Team 1"),
            new Team("Team 2"),
            // new Team("Team 3"),
            // new Team("Team 4"),
            // new Team("Team 5"),
            // new Team("Team 6"),
            // new Team("Team 7"),
            // new Team("Team 8"),
            // new Team("Team 9"),
            // new Team("Team 10"),
            // new Team("Team 11"),
            // new Team("Team 12"),
        ];

    static void Main()
    {
        Draft draft = new Draft(teams);

        shuffleDraft();

        draft.run();

    }

    public static void shuffleDraft()
    {
        Random random = new Random();
        
        for (int x = teams.Length - 1; x >= 0; x--)
        {
            int randomIndex = random.Next(x + 1);
            (teams[x], teams[randomIndex]) = (teams[randomIndex], teams[x]);
        }

    }
}
