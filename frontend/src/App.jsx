import {useEffect, useState} from 'react'
import axios from 'axios'
import './App.css'

function App(){
  const [players,setPlayers] = useState([])
  const [playerName, setPlayerName] = useState('')
  const [playerNumber, setPlayerNumber] = useState('')
  const [position, setPosition] = useState('GK')
  const [error, setError] = useState('')

  const API_URL = 'http://127.0.0.1:8000'

  //retrieve players from backend
  const fetchPlayers = async () => {
    try{
      const response = await axios.get(`${API_URL}/players`)
      setPlayers(response.data)
      setError('')
    } catch (error) {
      console.error('Error fetching players:', error)
      setError('Could not connect to the server. Check the backend')
    }
  }

  //Load players onto page
  useEffect(()=> {fetchPlayers()}, [])  

  //add new player
  const addPlayer = async (event) => {
    event.preventDefault()
    
    if (!playerName.trim() || !playerNumber) {
      setError('Please enter a player name and jersey number')
      return
    }
    
    try{
      await axios.post(`${API_URL}/players`, {
        player_name: playerName,
        player_number: Number(playerNumber),
        position: position
    })
    
    //clear the player form
    setPlayerName('')
    setPlayerNumber('')
    setPosition('GK')
    setError('')

    //refresh player list
    fetchPlayers()
  } catch (error) {
    console.error('Error adding player:', error)
    setError('Could not add player. Check entered details')
  }
  }


  //delete a player
  const deletePlayer = async (id) => {
    try{
      await axios.delete(`${API_URL}/players/${id}`)
      fetchPlayers()
    } catch (error){
      console.error('Error deleting player:', error)
      setError('Could not delete player')
    }
  }


  return (
    <div className="app-container">
      <header>
        <h1>Football XI Builder</h1>
        <p>Please choose your starting XI</p>
      </header>

      <section className="player-form-selection">
        <h2>Add a player</h2>

        <form onSubmit={addPlayer}>

          <input
            type = "text"
            placeholder = "Player name"
            value = {playerName}
            onChange = {(event) => setPlayerName(event.target.value)}
            minLength="2"
            maxLength="50"
            required
          />
          
          <input 
            type = "number"
            placeholder = "jersey number"
            value = {playerNumber}
            onChange = {(event) => setPlayerNumber(event.target.value)}
            minLength="2"
            maxLength="50"
            required
          />

          <select value={position} onChange={(event) => setPosition(event.target.value)}>
            <option value="GK">Goalkeeper</option>
            <option value="DEF">Defender</option>
            <option value="MID">Midfielder</option>
            <option value="FWD">Forward</option>
          </select>
          
          <button type="submit">Add Player</button>

        </form>
      </section>

      {error && <p className="error-message">{error}</p>}

      <section className="squad-section">
        <h2>Your Squad ({players.length} players)</h2>

        {players.length === 0?(
          <p>No players added yet</p>
        ):(
          <div className="player-list">
            {players.map((player) => (
              <div className="player-card" key={player.id}>
                <div className="player-number">
                  {player.player_number}
                </div>

                <div className="player-details">
                  <h3>{player.player_name}</h3>
                  <p>{player.position}</p>
                  <p>
                    {player.on_starting_xi ? 'Starting XI'
                    : 'Substitute'}
                  </p>
                </div>

                <button className="delete-button" onClick={() => deletePlayer(player.id)}

                >
                  Delete
                </button>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  )
}

export default App
