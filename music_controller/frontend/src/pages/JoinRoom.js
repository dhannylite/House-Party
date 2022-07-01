import { Button, TextField } from '@material-ui/core'
import React, { useRef, useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import './JoinRoom.css'

export default function JoinRoom() {
  const [enteredRoomCode, setEnteredRoomCode] = useState('')
  const [error, setError] = useState(null)
  const navigate = useNavigate()
  // const enteredRoomCodeRef = useRef()
  function enteredRoomCodeHandler(event) {
    setEnteredRoomCode(event.target.value)
  }

  async function joinRoomHandler() {
    const reqOpt = {
      method: 'POST',
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        code: enteredRoomCode
      })
    }
    const request = await fetch('/api/join-room', reqOpt)
    if (request.ok) {
      navigate(`/room/${enteredRoomCode}`)
    } else {
      setError('Room not found')
    }
  }
  return (
    <div className='join'>
      <h1>Join A Room</h1>
      <div>
        <TextField
          error={error}
          label='code'
          placeholder='Enter the Room Code'
          value={enteredRoomCode}
          variant='outlined'
          helperText={error}
          onChange={enteredRoomCodeHandler}
        />
      </div>
      <div className='join-btn'>
      <Button variant='contained' color='primary' onClick={joinRoomHandler}>Join Room</Button>
      </div>
      <div>
      <Button variant='contained' color='secondary' to='/' component={Link} >Back</Button>
      </div>
    </div>
  )
}

