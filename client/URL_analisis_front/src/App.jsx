import React, { useState } from 'react';
import PieChartComponent from './components/PieChartComponent';
import BarChartComponent from './components/BarChartComponent';

function AnalizarURLs() {
  const [url, setUrl] = useState('');
  const [file, setFile] = useState(null);
  const [urlAnalysisResult, setUrlAnalysisResult] = useState(null);
  const [csvAnalysisResult, setCsvAnalysisResult] = useState(null);
  const [loading, setLoading] = useState(false); // Estado de carga
  const [loading1, setLoading1] = useState(false); // Estado de carga
  const [total, setTotal] = useState({
    blackList: 0,
    characteristic: 0,
    similarity: 0,
    prediction: 0,
    safe: 0
  });


  const [message, setMessage] = useState('');
  // Función para manejar el análisis de una URL individual




  const analizarURL = async () => {
    try {
      setLoading(true); // Activa el estado de carga
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
      setLoading(false); // Desactiva el estado de carga
    } catch (error) {
      console.error('Error al analizar la URL:', error);
      setLoading(false); // Desactiva el estado de carga
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


  const getTotals = (data) => {
    const totals = {
      blackList: 0,
      characteristic: 0,
      similarity: 0,
      prediction: 0,
      safe: 0 // Añadir atributo para contar las predicciones que son 0
    };
  
    data.forEach((element) => {
      totals.blackList += element.blackList;
      totals.characteristic += element.characteristic;
      totals.similarity += element.similarity;
      totals.prediction += element.prediction;
      if (element.prediction === 0) {
        totals.safe += 1;
      }
    });
  
    return totals;
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
      setLoading1(true); // Activa el estado de carga
      const response = await fetch('http://127.0.0.1:5000/predictgroup', {
        method: 'POST',
        body: formData,
      });
      const data = await response.json();
      console.log(data)
      setTotal(getTotals(data));
      setCsvAnalysisResult(data); // Guarda el resultado del análisis
      setLoading1(false); // Desactiva el estado de carga
    } catch (error) {
      console.error('Error al analizar el CSV:', error);
      setLoading1(false); // Desactiva el estado de carga
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
          {loading && (
            <div className="flex justify-center items-center mt-4">
              <div className="animate-spin rounded-full h-10 w-10 border-4 border-gray-300 border-t-blue-500"></div>
            </div>
            )}
          {urlAnalysisResult && (
          <div className='flex justify-center'>
            {(() => {
              if (urlAnalysisResult[0] === 1) {
                return (
                  <div className='flex flex-col items-center'>
                    <div className='flex'>
                      <p className='font-bold'>Resultado del análisis:</p>
                      <p className='bg-red-600 ml-1'>Posible URL de phishing</p>
                    </div>
                    <div className='flex'>
                      <p className='font-bold'>Motivo:</p>
                      <p className='ml-1'>{urlAnalysisResult[1]}</p>
                    </div>
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
                    <p className='bg-green-600 ml-1'>URL segura</p>
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
          {loading1 && (
            <div className="flex justify-center items-center mt-4">
             <div className="animate-spin rounded-full h-10 w-10 border-4 border-gray-300 border-t-blue-500"></div>
            </div>
          )}
          {total.prediction > 0 ? (
            <div className='mt-20 space-y-10'>
              <strong>Tienes posibles URLs de phishing</strong>
              <div className='flex'>
                <PieChartComponent blackList={total.blackList} characteristic={total.characteristic} similarity={total.similarity} />
                <BarChartComponent positive={total.prediction} middle={total.characteristic} negative={total.safe} />
              </div>
            </div>
          ): (
            <div className='mt-20 space-y-10'>
              <strong>No tienes URLs de phishing</strong>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default AnalizarURLs;
