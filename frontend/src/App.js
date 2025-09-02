import "./App.css";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import TodoList from "./components/TodoList";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<TodoList />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
