'use client';
import { useState, useEffect } from 'react';

// api endpoint
const API_ENDPOINT = 'http://0.0.0.0:80';

export default function ManagementConsole() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [currentEventId, setCurrentEventId] = useState(null);

  // Poll the API every 5 seconds
  useEffect(() => {
    const fetchLatestData = async () => {
      try {
        const response = await fetch(`${API_ENDPOINT}/latest_event_id`);
        const result = await response.json();
        console.log(result);
        const latestEventId = result["id"];
        if (latestEventId) {
          if (latestEventId !== currentEventId) {
            console.log('Fetching latest data...');
            // Fetch the latest data
            const response = await fetch(`${API_ENDPOINT}/events`);
            const res = await response.json();
            setData(res.body);
            setCurrentEventId(latestEventId);
          }
        }
      } catch (error) {
        console.error('Error fetching data:', error);
        setError(error.message);
      }
    };
    fetchLatestData();
    const intervalId = setInterval(fetchLatestData, 5000); // Poll every 20 seconds

    return () => clearInterval(intervalId);
  }, [currentEventId]);

  return (
    <div style={{ padding: '20px', height: '100vh'}}>
      <h1>Management Console</h1>

      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {!loading && !error && (
        <table className='table-auto border border-slate-500' cellPadding="10" style={{ width: '100%', marginTop: '20px'}}>
          <thead>
            <tr className='bg-teal-500/50'>
              <th className='border border-slate-500'>Created At</th>
              <th className='border border-slate-500 '>Event ID</th>
              <th className='border border-slate-500'>Event Name</th>
              <th className='border border-slate-500'>Event data</th>
            </tr>
          </thead>
          <tbody>
            {data.length > 0 ? (
              data.map((item) => (
                <tr key={item[0]} className='event-row'>
                  <td className='border-slate-500 border-x'>{item[0]}</td>
                  <td className='border-slate-500 border-x'>{item[1]}</td>
                  <td className='border-slate-500 border-x'>{item[2]}</td>
                  <td className='border-slate-500 border-x'>{item[3]}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={3}>No data available</td>
              </tr>
            )}
          </tbody>
        </table>
      )}
    </div>
  );
}
