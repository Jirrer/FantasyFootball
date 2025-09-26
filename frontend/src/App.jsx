import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import DraftBoard from './components/DraftBoard'
import UserTeam from './components/UserTeam'
import PlayerBoard from './components/PlayerBoard'

function App() {
  const [active, setActive] = useState('PlayerBoard');

  return (
    <>
    <div className='topBar'>
      <button onClick={() => setActive('PlayerBoard')}>Draft</button>
      <button onClick={() => setActive('UserTeam')}>My Team</button>
      <button onClick={() => setActive('DraftBoard')}>Board</button>
    </div>
    {active === 'PlayerBoard' && <PlayerBoard />}
    {active === 'UserTeam' && <UserTeam />}
    {active === 'DraftBoard' && <DraftBoard />}
    </>
  )
}

export default App
