import { React, useContext } from "react";
import { AuthContext } from "./AuthContext";
import players from "../players.json";


const PlayerBoard = () => {
    const { user } = useContext(AuthContext);
    
    const makePick = async (pickData) => {
    try {
        const response = await fetch('/userPick', {
            method: 'POST',                 // Use POST to send data
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(pickData)  // Send the JSON data
        });

        const data = await response.json();
        console.log(data);
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
          {teamPlayers.map((player, index) => (
            <button
                key={`${player.name}-${player.position}-${index}`}
                className={player.position}
                onClick={() =>
                makePick({
                    username: user.name,
                    playerName: player.name,
                    team: player.team,
                    position: player.position
                })
                }
            >
                {player.name}
            </button>
            ))}
        </div>
      ))}
    </div>
  )
}

export default PlayerBoard