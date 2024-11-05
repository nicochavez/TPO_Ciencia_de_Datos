import React, { useState } from 'react';

function AnalizarURLs() {
  const [url, setUrl] = useState('');
  const [file, setFile] = useState(null);
  const [urlAnalysisResult, setUrlAnalysisResult] = useState(null);
  const [csvAnalysisResult, setCsvAnalysisResult] = useState(null);
  const [message, setMessage] = useState('');
  // Función para manejar el análisis de una URL individual
  const analizarURL = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/predict', {
        method: "POST",
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });
      const data = await response.json();
      console.log(data)
      setUrlAnalysisResult(data); // Guarda el resultado del análisis
      alert(data);
    } catch (error) {
      console.error('Error al analizar la URL:', error);
    }
  };

  const fetchMessage = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/');
      if (response.ok) {
        const text = await response.text();
        setMessage(text);
      } else {
        setMessage('Error al conectar con el backend respuesta mala');
      }
    } catch (error) {
      setMessage('Error al conectar con elsdfsfsdfsdfd backend');
    }
  };


  // Función para manejar el análisis de un archivo CSV
  const analizarCSV = async () => {
    if (!file) {
      alert('Por favor, selecciona un archivo CSV');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:5000/predictgroup', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      setCsvAnalysisResult(data); // Guarda el resultado del análisis
      alert(data);
    } catch (error) {
      console.error('Error al analizar el CSV:', error);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>Analizador de URLs</h1>

      {/* Formulario para analizar una URL individual */}
      <div style={{ marginBottom: '20px' }}>
        <h2>Análisis de una URL individual</h2>
        <input
          type="text"
          placeholder="Introduce la URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={{ marginRight: '10px' }}
        />
        <button onClick={analizarURL}>Analizar URL</button>
        {urlAnalysisResult && (
          <div style={{ marginTop: '10px' }}>
            <strong>Resultado del análisis:</strong> {JSON.stringify(urlAnalysisResult)}
          </div>
        )}
      </div>

      {/* Formulario para analizar un archivo CSV */}
      <div style={{ marginBottom: '20px' }}>
        <h2>Análisis de un archivo CSV</h2>
        <input
          type="file"
          accept=".csv"
          onChange={(e) => setFile(e.target.files[0])}
          style={{ marginRight: '10px' }}
        />
        <button onClick={analizarCSV}>Analizar CSV</button>
        {csvAnalysisResult && (
          <div style={{ marginTop: '10px' }}>
            <strong>Resultado del análisis:</strong> {JSON.stringify(csvAnalysisResult)}
          </div>
        )}
      </div>
      <div style={{ textAlign: 'center', marginTop: '20px' }}>
        <button onClick={fetchMessage}>Mostrar mensaje</button>
        {message && <p>{message}</p>}
      </div>
    </div>
  );
}

export default AnalizarURLs;
