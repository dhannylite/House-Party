import CreateRoom from "./pages/CreateRoom";
import HomePage from "./pages/HomePage";
import JoinRoom from "./pages/JoinRoom";
import {Routes, Route, Navigate} from 'react-router-dom'
import Room from "./pages/Room";
import { useEffect, useState } from "react";

function App() {
  const [roomCode, setRoomCode] = useState(null)
  // useEffect(() => {
  //   async function userInRoom() {
  //     const response = await fetch('/api/user-in-room')
  //     const data = await response.json()
  //     console.log(data)
  //     setRoomCode(data.code)
  //   }
  //   userInRoom()
  // }, [])
  function setRoomHandler(code) {
    setRoomCode(code)
  }
  function clearRoomCode() {
    setRoomCode(null)
  }
  console.log(roomCode)
  return (
    <div>
      <Routes>
        <Route path='/' element={!roomCode ? <HomePage onSet={setRoomHandler} /> : <Navigate to={`/room/${roomCode}`} />} />
        <Route path='/join' element={<JoinRoom />} />
        <Route path='/create' element={<CreateRoom />} />
        <Route path="/room/:code" element={<Room onClear={clearRoomCode} />} />
      </Routes>
    </div>
  );
}
// !roomCode ? <HomePage /> : <Navigate replace to={`/room/${roomCode}`} 
export default App;
