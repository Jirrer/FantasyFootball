import { useEffect, useContext, useState, useCallback } from "react";
import { AuthContext } from "./AuthContext";
import players from "../players.json";

// potential issue - wont let you draft a player with the same name position and team

const PlayerBoard = () => {
  const { user } = useContext(AuthContext);
  const [nonAvailablePlayers, setNonAvailablePlayers] = useState([]);

  const getAvailablePlayers = useCallback(async () => {
    try {
      const res = await fetch("/getAvailablePlayers", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: user.name }),
      });

      const data = await res.json();

      // If NonAvailablePlayers is a JSON string, parse it
      const playersArray = Array.isArray(data.NonAvailablePlayers)
        ? data.NonAvailablePlayers
        : typeof data.NonAvailablePlayers === "string"
        ? JSON.parse(data.NonAvailablePlayers)
        : [];

      setNonAvailablePlayers(playersArray);

    } catch (err) {
      console.error("Error fetching available players:", err);
    }
  }, [user.name]);

  // Fetch on mount
  useEffect(() => {
    getAvailablePlayers();
  }, [getAvailablePlayers]);


  const makePick = async (pickData) => {
    try {
      const response = await fetch("/userPick", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(pickData),
      });

      await getAvailablePlayers(); // refresh unavailable players after pick
      const data = await response.json();
      console.log("Pick response:", data);
    } catch (error) {
      console.error("Error:", error);
    }
  };

  const teams = {};
  players.forEach((p) => {
    if (!teams[p.team]) teams[p.team] = [];
    teams[p.team].push(p);
  });

  return (
    <div className="playerBoard">
      {Object.entries(teams).map(([teamName, teamPlayers]) => (
        <div key={teamName} className="nflTeam">
          <h1>{teamName}</h1>
          {teamPlayers.map((player, index) => {
              // Check if this player's name exists in nonAvailablePlayers
              const isUnavailable = nonAvailablePlayers.some(
                (p) =>
                  p.name === player.name &&
                  p.position === player.position &&
                  p.team === player.team
              );

              return (
                <button
                  key={`${player.name}-${player.position}-${player.team}-${index}`} // unique key
                  className={`${player.position} ${isUnavailable ? "unavailable-player" : ""}`}
                  onClick={() =>
                    makePick({
                      username: user.name,
                      playerName: player.name,
                      team: player.team,
                      position: player.position,
                    })
                  }
                >
                  {player.name} - {player.position}
                </button>
              );
            })}
        </div>
      ))}
    </div>
  );
}

export default PlayerBoard;
