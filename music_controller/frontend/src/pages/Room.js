import { Button } from '@material-ui/core'
import React, { useEffect, useState } from 'react'
import { useParams, Link, useNavigate } from 'react-router-dom'
import MusicPlayer from '../components/MusicPlayer'
import CreateRoom from './CreateRoom'
import './Room.css'

export default function Room(props) {
    const params = useParams()
    const { code } = params
    const [isHost, setIsHost] = useState(false)
    const navigate = useNavigate()
    const [guestCanPause, setGuestCanPause] = useState(true)
    const [voteToSkip, setVoteToSkip] = useState(2)
    const [showSettings, setShowSettings] = useState(false)
    const [isAuthenticated, setIsAuthenticated] = useState(false)
    const [song, setSong] = useState()
    getRoomDetails()
    useEffect(() => {
        const interval = setInterval(() => {
            async function getCurretSong() {
                const response = await fetch('/spotify/current-song')
                const data = await response.json()
                setSong(data)
                console.log(data)
            }
            getCurretSong()
        
    }, 1000)
        return () => {
            clearInterval(interval)
        }
        
    }, [])
    
    async function getRoomDetails() {
        console.log(1)
        const response = await fetch(`/api/get-room?code=${code}`)
        if (!response.ok) {
            navigate('/')
        }
        const data = await response.json()
        console.log(data, 3)
        setIsHost(data.is_Host)
        setGuestCanPause(data.guest_can_pause)
        setVoteToSkip(data.vote_to_skip)
        if (isHost) {
            isAuthenticatedHandler()
        }
    }
    
    async function isAuthenticatedHandler() {
        const response = await fetch('/spotify/is-authenticated')
        const data = await response.json()
        console.log(data,'kiil')
        setIsAuthenticated(data.status)
        if (!data.status) {
            const response = await fetch('/spotify/get-auth-url')
            const data = await response.json()
            window.location.replace(data.url)
        }
    }

    // async function getCurretSong() {
    //     const response = await fetch('/spotify/current-song')
    //     const data = await response.json()
    //     setSong(data)
    //     console.log(data)
    // }

    async function leaveRoomHandler() {
        const reqOpt = {
            method: "POST",
            headers: {"Content-Type": "application/json"}
        }
        const response = await fetch('/api/leave-room', reqOpt)
        const data = await response.json()
        props.onClear()
        navigate('/')
    }

    function showSettingsHandler() {
        setShowSettings(true)
    }
    if (showSettings) {
        return <div className='settings'>
            <CreateRoom update={true} voteToSkip={voteToSkip} guestCanPause={guestCanPause} roomCode={code} />
            <Button variant='contained' color='secondary' onClick={() => {setShowSettings(false)}}>Close</Button>
        </div>
    }
  return (
      <div className='room'>
          <MusicPlayer {...song} />
          {/* <p>room code: {code}</p>
          <p>votes: {voteToSkip}</p>
          <p>Guess Can Pause: {guestCanPause.toString()}</p>
          <p>isHost: {isHost.toString()}</p> */}
          {isHost && <Button onClick={showSettingsHandler} variant='contained' color='primary' className='setting'>Settings</Button>}
          <Button variant='contained' color='secondary' onClick={leaveRoomHandler}>Leave Room</Button>
      </div>
  )
}
