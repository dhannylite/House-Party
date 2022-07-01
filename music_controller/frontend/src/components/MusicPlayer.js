import { Card, LinearProgress, IconButton } from '@material-ui/core'
import React from 'react'
import { PlayArrow } from '@material-ui/icons'
import { Pause } from '@material-ui/icons'
import { SkipNext } from '@material-ui/icons'
import { SkipPrevious } from '@material-ui/icons'
import './MusicPlayer.css'

export default function MusicPlayer(props) {
    const songProgress = props.time / props.duration * 100
    function playSong() {
        fetch('/spotify/play', {
            method: 'PUT',
            headers: {"Content-Type": "application/json"}
        })
    }
    function pauseSong() {
        fetch('/spotify/pause', {
            method: 'PUT',
            headers: {"Content-Type": "application/json"}
        })
    }
    function skipSong() {
        fetch('/spotify/skip', {
            method: 'POST',
            headers: {"Content-Type": "application/json"}
        })
    }
    function previousSong() {
        fetch('/spotify/previous', {
            method: 'POST',
            headers: {"Content-Type": "application/json"}
        })
    }
    function SearchSong(event) {
        event.preventDefault()
        fetch('/spotify/search')
    }

    return (
        <>
          {/* <form onSubmit={SearchSong}>
                <input type='text' />
                <button>search</button>
            </form> */}
      <div className='card'>
          <div className='card-img-box'>
              <img src={props.image_url} alt="albulm cover"/>
          </div>
          <div className='content'>
              
          <div>
              <h2>{props.title}</h2>
          </div>
          <div>
              <h6>{props.artists}</h6>
              </div>
              <IconButton className='btn' onClick={previousSong}>
                  <SkipPrevious /> 
              </IconButton>
          <IconButton className='btn' onClick={props.is_playing ? pauseSong : playSong}>
              {props.is_playing ? <Pause/> : <PlayArrow />}
          </IconButton>
          <IconButton className='btn' onClick={skipSong}>
                  <SkipNext /> 
              </IconButton>
              <div className='votes'>
                vote to skip: {props.votes} / {props.votes_required}
              </div>
          <div>
              <LinearProgress variant='determinate' value={songProgress}/>
          </div>
          </div>
    </div>
      </>
  )
}
