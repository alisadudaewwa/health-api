import { useState } from 'react';

function App() {
  const [name, setName] = useState('');
  const [userId, setUserId] = useState(null);
  const [metrics, setMetrics] = useState([]);
  const [newMetric, setNewMetric] = useState({ type: 'pulse', value: '' });

  // Создание пользователя
  const createUser = async () => {
    try {
      const response = await fetch('http://localhost:8001/users', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name }),
      });
      const data = await response.json();
      setUserId(data.id);
      alert(`Пользователь создан! ID: ${data.id}`);
    } catch (error) {
      alert('Ошибка: ' + error.message);
    }
  };

  // Добавление метрики
  const addMetric = async (e) => {
    e.preventDefault();
    if (!userId) {
      alert('Сначала создайте пользователя!');
      return;
    }
    try {
      const response = await fetch(`http://localhost:8001/metrics?user_id=${userId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          type: newMetric.type,
          value: parseFloat(newMetric.value)
        }),
      });
      const data = await response.json();
      setNewMetric({ type: 'pulse', value: '' });
      loadMetrics();
      alert('Метрика добавлена!');
    } catch (error) {
      alert('Ошибка: ' + error.message);
    }
  };

  // Загрузка метрик
  const loadMetrics = async () => {
    if (!userId) return;
    try {
      const response = await fetch(`http://localhost:8001/metrics/${userId}`);
      const data = await response.json();
      setMetrics(data);
    } catch (error) {
      console.error('Ошибка загрузки:', error);
    }
  };

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: '0 auto' }}>
      <h1>🏥 Health Metrics Tracker</h1>

      {/* Создание пользователя */}
      <div style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
        <h2>1️⃣ Регистрация</h2>
        <input
          placeholder="Введите ваше имя"
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={{ padding: '10px', marginRight: '10px', width: '200px' }}
        />
        <button onClick={createUser} style={{ padding: '10px 20px' }}>
          Создать пользователя
        </button>
        {userId && <p style={{ color: 'green', marginTop: '10px' }}>✅ Ваш ID: {userId}</p>}
      </div>

      {/* Добавление метрики */}
      {userId && (
        <div style={{ marginBottom: '30px', padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
          <h2>2️⃣ Добавить показатель</h2>
          <form onSubmit={addMetric}>
            <select
              value={newMetric.type}
              onChange={(e) => setNewMetric({ ...newMetric, type: e.target.value })}
              style={{ padding: '10px', marginRight: '10px' }}
            >
              <option value="pulse">❤️ Пульс</option>
              <option value="weight">⚖️ Вес (кг)</option>
              <option value="height">📏 Рост (см)</option>
              <option value="pressure">💓 Давление</option>
              <option value="sleep">😴 Сон (минут)</option>
              <option value="glucose">🩸 Глюкоза</option>
              <option value="stress">😰 Стресс</option>
            </select>
            <input
              type="number"
              step="0.1"
              placeholder="Значение"
              value={newMetric.value}
              onChange={(e) => setNewMetric({ ...newMetric, value: e.target.value })}
              style={{ padding: '10px', marginRight: '10px' }}
              required
            />
            <button type="submit" style={{ padding: '10px 20px' }}>
              Добавить
            </button>
          </form>
        </div>
      )}

      {/* Список метрик */}
      {userId && (
        <div style={{ padding: '20px', border: '1px solid #ddd', borderRadius: '8px' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <h2>📊 Ваши показатели</h2>
            <button onClick={loadMetrics} style={{ padding: '10px 20px' }}>
              Обновить
            </button>
          </div>
          {metrics.length === 0 ? (
            <p>Пока нет данных. Добавьте первую метрику!</p>
          ) : (
            <ul style={{ listStyle: 'none', padding: 0 }}>
              {metrics.map((m) => (
                <li key={m.id} style={{
                  padding: '10px',
                  marginBottom: '10px',
                  backgroundColor: '#f5f5f5',
                  borderRadius: '4px'
                }}>
                  <strong>{m.type}</strong>: {m.value}
                  <small style={{ color: '#666', marginLeft: '10px' }}>
                    ({new Date(m.timestamp).toLocaleString()})
                  </small>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}

export default App;