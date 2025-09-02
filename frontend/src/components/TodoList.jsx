import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Card, CardContent } from '@/components/ui/card';
import { Checkbox } from '@/components/ui/checkbox';
import { Trash2, Plus } from 'lucide-react';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const API = `${API_BASE}/api`;

const TodoList = () => {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchTodos = async () => {
    try {
      const response = await axios.get(`${API}/todos`);
      setTodos(response.data);
    } catch (error) {
      console.error('Error fetching todos:', error);
    }
  };

  const addTodo = async () => {
    if (!newTodo.trim()) return;
    
    setLoading(true);
    try {
      const response = await axios.post(`${API}/todos`, { text: newTodo });
      setTodos([response.data, ...todos]);
      setNewTodo('');
    } catch (error) {
      console.error('Error adding todo:', error);
    }
    setLoading(false);
  };

  const toggleTodo = async (id, completed) => {
    try {
      const response = await axios.put(`${API}/todos/${id}`, { completed: !completed });
      setTodos(todos.map(todo => 
        todo.id === id ? { ...todo, completed: !completed } : todo
      ));
    } catch (error) {
      console.error('Error updating todo:', error);
    }
  };

  const deleteTodo = async (id) => {
    try {
      await axios.delete(`${API}/todos/${id}`);
      setTodos(todos.filter(todo => todo.id !== id));
    } catch (error) {
      console.error('Error deleting todo:', error);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      addTodo();
    }
  };

  useEffect(() => {
    fetchTodos();
  }, []);

  return (
    <div className="min-h-screen bg-cover bg-center bg-fixed flex items-center justify-center p-4" 
         style={{ backgroundImage: 'url(https://storage.googleapis.com/fenado-ai-farm-public/generated/90eafb26-2e44-4f98-a56f-d81136c16944.webp)' }}>
      <Card className="w-full max-w-2xl bg-white/90 backdrop-blur-sm shadow-2xl border-0">
        <CardContent className="p-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-8 text-center">
            ✨ Todo List
          </h1>
          
          <div className="flex gap-3 mb-8">
            <Input
              type="text"
              placeholder="Add a new todo..."
              value={newTodo}
              onChange={(e) => setNewTodo(e.target.value)}
              onKeyPress={handleKeyPress}
              className="flex-1 text-lg py-6 px-4 border-2 border-gray-200 focus:border-blue-400 rounded-xl"
            />
            <Button 
              onClick={addTodo} 
              disabled={loading || !newTodo.trim()}
              className="px-6 py-6 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white rounded-xl shadow-lg hover:shadow-xl transition-all duration-200"
            >
              <Plus className="w-5 h-5" />
            </Button>
          </div>

          <div className="space-y-3 max-h-96 overflow-y-auto">
            {todos.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-gray-500 text-lg">No todos yet. Add one above! 🚀</p>
              </div>
            ) : (
              todos.map((todo) => (
                <div 
                  key={todo.id} 
                  className="flex items-center gap-4 p-4 bg-white/70 rounded-xl border border-gray-200 hover:bg-white/90 transition-all duration-200 group"
                >
                  <Checkbox
                    checked={todo.completed}
                    onCheckedChange={() => toggleTodo(todo.id, todo.completed)}
                    className="w-5 h-5"
                  />
                  <span 
                    className={`flex-1 text-lg ${
                      todo.completed 
                        ? 'line-through text-gray-500' 
                        : 'text-gray-800'
                    } transition-all duration-200`}
                  >
                    {todo.text}
                  </span>
                  <Button
                    variant="ghost"
                    size="sm"
                    onClick={() => deleteTodo(todo.id)}
                    className="opacity-0 group-hover:opacity-100 text-red-500 hover:text-red-700 hover:bg-red-50 transition-all duration-200"
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              ))
            )}
          </div>

          {todos.length > 0 && (
            <div className="mt-6 text-center text-sm text-gray-600">
              {todos.filter(todo => !todo.completed).length} of {todos.length} tasks remaining
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  );
};

export default TodoList;