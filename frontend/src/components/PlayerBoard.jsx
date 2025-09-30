import React from 'react'

const PlayerBoard = () => {
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

  return (
    <div className='playerBoard'>
        <div className='nflTeam'>
            <h1>Buffalo Bills</h1>
            <button className='QB' onClick={() => makePick({username: 'testusername', playerName: 'Josh Allen', team: 'Bills', position: 'QB'})}>Josh Allen</button>
            <button className='QB'>test</button>
            <button className='WR'>test</button>
            <button className='WR'>test</button>
            <button className='WR'>test</button>
            <button className='RB'>test</button>
            <button className='RB'>test</button>
            <button className='RB'>test</button>
            <button className='TE'>test</button>
            <button className='TE'>test</button>
            <button className='K'>test</button>
            <button className='DFS'>test</button>
        </div>
        <div className='nflTeam'>
            <div className='QB'>test</div>
            <div className='QB'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='TE'>test</div>
            <div className='TE'>test</div>
            <div className='K'>test</div>
            <div className='DFS'>test</div>
        </div>
        <div className='nflTeam'>
            <div className='QB'>test</div>
            <div className='QB'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='TE'>test</div>
            <div className='TE'>test</div>
            <div className='K'>test</div>
            <div className='DFS'>test</div>
        </div>
        <div className='nflTeam'>
            <div className='QB'>test</div>
            <div className='QB'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='TE'>test</div>
            <div className='TE'>test</div>
            <div className='K'>test</div>
            <div className='DFS'>test</div>
        </div>
        <div className='nflTeam'>
            <div className='QB'>test</div>
            <div className='QB'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='TE'>test</div>
            <div className='TE'>test</div>
            <div className='K'>test</div>
            <div className='DFS'>test</div>
        </div>
        <div className='nflTeam'>
            <div className='QB'>test</div>
            <div className='QB'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='TE'>test</div>
            <div className='TE'>test</div>
            <div className='K'>test</div>
            <div className='DFS'>test</div>
        </div>
        <div className='nflTeam'>
            <div className='QB'>test</div>
            <div className='QB'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='TE'>test</div>
            <div className='TE'>test</div>
            <div className='K'>test</div>
            <div className='DFS'>test</div>
        </div>
        <div className='nflTeam'>
            <div className='QB'>test</div>
            <div className='QB'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='TE'>test</div>
            <div className='TE'>test</div>
            <div className='K'>test</div>
            <div className='DFS'>test</div>
        </div>
        <div className='nflTeam'>
            <div className='QB'>test</div>
            <div className='QB'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='TE'>test</div>
            <div className='TE'>test</div>
            <div className='K'>test</div>
            <div className='DFS'>test</div>
        </div>
        <div className='nflTeam'>
            <div className='QB'>test</div>
            <div className='QB'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='TE'>test</div>
            <div className='TE'>test</div>
            <div className='K'>test</div>
            <div className='DFS'>test</div>
        </div>
        <div className='nflTeam'>
            <div className='QB'>test</div>
            <div className='QB'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='TE'>test</div>
            <div className='TE'>test</div>
            <div className='K'>test</div>
            <div className='DFS'>test</div> 
        </div>
        <div className='nflTeam'>
            <div className='QB'>test</div>
            <div className='QB'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='TE'>test</div>
            <div className='TE'>test</div>
            <div className='K'>test</div>
            <div className='DFS'>test</div>
        </div>
        <div className='nflTeam'>
            <div className='QB'>test</div>
            <div className='QB'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='TE'>test</div>
            <div className='TE'>test</div>
            <div className='K'>test</div>
            <div className='DFS'>test</div>
        </div>
        <div className='nflTeam'>
            <div className='QB'>test</div>
            <div className='QB'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='WR'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='RB'>test</div>
            <div className='TE'>test</div>
            <div className='TE'>test</div>
            <div className='K'>test</div>
            <div className='DFS'>test</div>
        </div>


    </div>
  )
}

export default PlayerBoard