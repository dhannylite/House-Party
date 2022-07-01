import React, { useState } from 'react'
import './CreateRoom.css'
import FormControl from '@material-ui/core/FormControl'
import { Collapse, FormControlLabel, Radio, RadioGroup } from '@material-ui/core'
import { Link, useNavigate } from 'react-router-dom'
import {Alert} from '@material-ui/lab'


export default function CreateRoom(props) {
  const defaultValue = 2
  const [guestCanPause, setGuestCanPause] = useState(props.update ? props.guestCanPause : true)
  const [voteToSkip, setVoteToSkip] = useState(props.update ? props.voteToSkip : defaultValue)
  const [error, setError] = useState()
  const [message, setMessage] = useState()
  const navigate = useNavigate()

  // console.log(guestCanPause)
  function guestCanPauseHandler(event) {
    setGuestCanPause(prev => {
      return event.target.value === 'true' ? true : false
    })
  }
  function voteToSkipHandler(event) {
    setVoteToSkip(event.target.value)
  }

  async function createRoomHandler() {
    const reqOpt = {
      method: 'POST',
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        guest_can_pause: guestCanPause,
        vote_to_skip: voteToSkip
      })
    }

    const response = await fetch('/api/create', reqOpt)
    const data = await response.json()
    navigate(`/room/${data.code}`)
    console.log(voteToSkip)
  }

  async function updateRoomHandler() {
    const reqOpt = {
      method: 'PATCH',
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        guest_can_pause: guestCanPause,
        vote_to_skip: voteToSkip,
        code: props.roomCode
      })
    }
    const response = await fetch('/api/update-room', reqOpt)
    if (response.ok) {
      setMessage('Room Updated Successfully')
    } else {
      setError('Something went wrong')
    }
    const data = await response.json()
  }
  const title = props.update ? 'Update Room' : 'Create A Room'
  return (
    <div className='create'>
      <Collapse in={error || message}>
        {message ? <Alert severity='success' onClose={() => setMessage(null)}>{message}</Alert> : <Alert severity='error' onClose={() => setError(null)}>{error}</Alert> }
      </Collapse>
      <p>{title}</p>
      <span>Guest Control of Playback State</span>
      <form>
        <RadioGroup row defaultValue={props.update ? props.guestCanPause.toString() : 'true'} onChange={guestCanPauseHandler}>
          <FormControlLabel className='input' value='true' control={<Radio color='primary' />}
            label='play/pause'
            labelPlacement='bottom'
          />
          <FormControlLabel className='input' value='false' control={<Radio color='secondary' />}
            label='No control'
            labelPlacement='bottom'
          />
        </RadioGroup>
      </form>
      <form>
        <input type='number' value={voteToSkip} min='1' max='5' step='.1' onChange={voteToSkipHandler}/>
        <label>Votes Required To Skip Song</label>
      </form>
      {!props.update && <button className='create-btn' onClick={createRoomHandler}>Create A Room</button>}
      {props.update && <button className='create-btn' onClick={updateRoomHandler}>Update Room</button>}
     {!props.update && <Link className='back' to='/' >BACK</Link>}
    </div>
  )
}
