import { Button } from '@material-ui/core'
import React, { useEffect } from 'react'
import './HomePage.css'
import { Link } from 'react-router-dom'

export default function HomePage(props) {
  useEffect(() => {
    async function userInRoom() {
      const response = await fetch('/api/user-in-room')
      const data = await response.json()
      console.log(data)
      props.onSet(data.code)
    }
    userInRoom()
  }, [])

  return (
    <div className='home'>
      <h1>
        House Party
      </h1>
      <div>
        <Button variant='contained' color='primary' to='/join' component={Link}>JOIN A ROOM</Button>
        <Button  variant='contained' color='secondary' to='/create' component={Link}>CREATE A ROOM</Button>
      </div>
    </div>
  )
}
