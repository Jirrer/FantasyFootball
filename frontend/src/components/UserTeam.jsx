import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from './AuthContext';

const UserTeam = () => {
  const { user } = useContext(AuthContext);
  const [userTeam, setUserTeam] = useState([]);

  useEffect(() => {
    const fetchUserTeam = async () => {
      const res = await fetch("/pullUserTeam", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: user.name })
      });

      const data = await res.json();
      setUserTeam(data.picks); // schedules state update
    };

    fetchUserTeam();
  }, [user]); // fetch once when user exists

  useEffect(() => {
  }, [userTeam]); // logs whenever state changes

  const positionOrder = ["QB", "WR", "RB", "TE", "DFS", "K"];

  return (
    <div className='userTeam'>
      {userTeam
        .slice()
        .sort((a, b) => positionOrder.indexOf(a.position) - positionOrder.indexOf(b.position))
        .map((p, i) => (
          <div key={i} className="userTeamBox">
            {p.name} | {p.position} | {p.team}
          </div>
        ))
      }
    </div>
  );
};

export default UserTeam;
