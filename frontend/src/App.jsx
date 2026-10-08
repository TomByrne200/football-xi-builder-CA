import {useEffect, useState} from 'react'
import axios from 'axios'
import './App.css'

function App(){
  const [tasks,setTasks] = useState([])
  const [title, setTitle] = useState('')
  const [description, setDescription] = useState('')

  const fetchTasks = async () => {
    const response = await axios.get('http://127.0.0.1:8000/tasks')
    setTasks(response.data)
  }
  useEffect(()=> {fetchTasks()
  }, [])

  const addTask = async (event) => {
    event.preventDefault()

    if (!title.trim()) {
      return
    }

    await axios.post('http://127.0.0.1:8000/tasks', {
      title: title,
      description: description,
      completed: false
    })

    setTitle('')
    setDescription('')

    fetchTasks()
  }

  const toggleTask = async (task) => {
    await axios.put(`http://127.0.0.1:8000/tasks/${task.id}`, {
      title: task.title, 
      description: task.description,
      completed: !task.completed
    })
    fetchTasks()
  }

  const deleteTask = async (id) => {
    await axios.delete(`http://127.0.0.1:8000/tasks/${id}`)
    fetchTasks()
  }


  return (
    <div>
      <h1>Task Manager</h1>

      <form onSubmit={addTask}>
        <input 
          type = "text"
          placeholder = "Task title"
          value = {title}
          onChange = {(event) => setTitle(event.target.value)}
        />

        <input 
          type = "text"
          placeholder = "Task description"
          value = {description}
          onChange = {(event) => setDescription(event.target.value)}
        />

        <button type="submit">Add Task</button>
      </form>

      {tasks.map((task) => (
        <div key = {task.id}>
          <h2>{task.title}</h2>
          <p>{task.description}</p>
          <p>
            Status: {task.completed ? 'Completed' : 'Not Completed'}
          </p>

          <button onClick={() => toggleTask(task)}>
            {task.completed ? 'Mark as Not Completed' : 'Mark as Completed'}
          </button>

          <button onClick = {() => deleteTask(task.id)}>
            Delete
          </button>
        </div>
      ))}
    </div>
  )
}

export default App
