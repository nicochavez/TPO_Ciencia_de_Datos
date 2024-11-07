import React, { useState } from 'react';
import PieChartComponent from './components/PieChartComponent';
import BarChartComponent from './components/BarChartComponent';

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
    } catch (error) {
      console.error('Error al analizar el CSV:', error);
    }
  };

  return (
    <div className='bg-gray-900 text-white p-10 min-h-screen'>
    <h1 className='text-center text-3xl'>Analizador de URLs</h1>
    <div className= 'h-fit justify-center items-center mt-20 space-y-20'>
        {/* Formulario para analizar una URL individual */}
        <div className='bg-gray-800 text-center space-y-4  p-10 rounded-xl w-7/12 mx-auto '>
          <h2 className='text-xl'>Análisis de una URL individual</h2>
          <input
            type="text"
            placeholder="Introduce la URL"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            className='block w-1/2 mx-auto p-2 bg-gray-900'
          />
          <button onClick={analizarURL} className='block w-1/3 mx-auto p-2 bg-gray-700 rounded'>Analizar URL</button>
          {urlAnalysisResult && (
          <div className='flex justify-center'>
            {(() => {
              if (urlAnalysisResult[0] === 1) {
                return (
                  <div className='flex'>
                    <p className='font-bold'>Resultado del análisis:</p>
                    <p className='bg-red-600'>Posible URL de phishing</p>
                  </div>
                );
              } else if (urlAnalysisResult[0] === -1) {
                return (
                  <div className='flex'>
                    <p className='font-bold'>Resultado del análisis:</p>
                    <p className='bg-yellow-600'>URL no Valida</p>
                  </div>
                );
              } else {
                return (
                  <div className='flex'>
                    <p className='font-bold'>Resultado del análisis:</p>
                    <p className='bg-green-600'>URL segura</p>
                  </div>
                );
              }
            })()}
          </div>
        )}


        </div>

        {/* Formulario para analizar un archivo CSV */}
        <div className='bg-gray-800 text-center space-y-4 p-10 rounded-xl w-7/12 mx-auto '>
          <h2 className='text-xl'>Análisis de un archivo CSV</h2>
          <input
            type="file"
            accept=".csv"
            onChange={(e) => setFile(e.target.files[0])}
            className='block w-5/12 mx-auto p-2 bg-gray-900'
          />
          <button onClick={analizarCSV} className='block w-1/3 mx-auto p-2 bg-gray-700 rounded'>Analizar CSV</button>
          {csvAnalysisResult && (
            <div className='mt-20 space-y-10'>
              <strong>Tienes {csvAnalysisResult[0]} posibles URLs de phishing</strong>
              <div className='flex'>
                <PieChartComponent positive={csvAnalysisResult[0]} negative={csvAnalysisResult[1]} />
                <BarChartComponent positive={csvAnalysisResult[0]} negative={csvAnalysisResult[1]} />
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default AnalizarURLs;
