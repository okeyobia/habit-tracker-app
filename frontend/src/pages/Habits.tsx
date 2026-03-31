import { useEffect, useState } from 'react';
import { getHabits, createHabit, updateHabit, deleteHabit, trackHabit } from '../api';

interface Habit {
  id: number;
  name: string;
  description?: string;
}

export default function Habits({ token }: { token: string }) {
  const [habits, setHabits] = useState<Habit[]>([]);
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchHabits = async () => {
    setLoading(true);
    setError('');
    try {
      const res = await getHabits(token);
      setHabits(res.data);
    } catch (err: any) {
      setError('Failed to fetch habits');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHabits();
    // eslint-disable-next-line
  }, [token]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      await createHabit(token, { name, description });
      setName('');
      setDescription('');
      fetchHabits();
    } catch (err: any) {
      setError('Failed to create habit');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id: number) => {
    setLoading(true);
    setError('');
    try {
      await deleteHabit(token, id);
      fetchHabits();
    } catch (err: any) {
      setError('Failed to delete habit');
    } finally {
      setLoading(false);
    }
  };

  // For brevity, update and track handlers can be added similarly

  return (
    <div>
      <h2>Your Habits</h2>
      {loading && <div>Loading...</div>}
      {error && <div style={{ color: 'red' }}>{error}</div>}
      <ul>
        {habits.map(habit => (
          <li key={habit.id}>
            <b>{habit.name}</b> {habit.description}
            <button onClick={() => handleDelete(habit.id)}>Delete</button>
            {/* Add update and track buttons here */}
          </li>
        ))}
      </ul>
      <form onSubmit={handleCreate}>
        <input
          type="text"
          placeholder="Habit name"
          value={name}
          onChange={e => setName(e.target.value)}
          required
        />
        <input
          type="text"
          placeholder="Description (optional)"
          value={description}
          onChange={e => setDescription(e.target.value)}
        />
        <button type="submit" disabled={loading}>Add Habit</button>
      </form>
    </div>
  );
}
