import React from 'react';
import { FaFlask } from 'react-icons/fa';

const generatedTests = [
    { id: 1, title: 'Тест 1', description: 'Математика - Основно ниво' },
    { id: 2, title: 'Тест 2', description: 'Физика - Средно ниво' },
    { id: 3, title: 'Тест 3', description: 'Хемија - Напредно ниво' },
    { id: 4, title: 'Тест 4', description: 'Историја - Краток квиз' },
    { id: 5, title: 'Тест 5', description: 'Географија - Основно ниво' },
    { id: 6, title: 'Тест 6', description: 'Биологија - Напредно ниво' },
    { id: 7, title: 'Тест 7', description: 'Информатика - Практичен тест' },
];

const GeneratedContentCard = () => {
    return (
        <>
            <style>{`
        .card-container {
          display: grid;
          grid-template-columns: repeat(3, 240px);
          gap: 20px;
          padding: 20px;
          justify-content: center;
        }
        .card {
          background-color: #ffffff;
          padding: 20px;
          border-radius: 16px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
          transition: box-shadow 0.3s ease;
          text-align: center;
        }
        .card:hover {
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        }
        .card-header {
          display: flex;
          align-items: center;
          margin-bottom: 10px;
        }
        .card-icon {
          color: #16a34a;
          font-size: 20px;
          margin-right: 10px;
        }
        .card-title {
          color: #1d4ed8;
          font-weight: bold;
          font-size: 16px;
          text-align: center;
        }
        .card-description {
          color: #4b5563;
          font-size: 14px;
        }
      `}</style>

            <div className="card-container">
                {generatedTests.map((test) => (
                    <div key={test.id} className="card">
                        <div className="card-header">
                            <FaFlask className="card-icon" />
                            <h3 className="card-title">{test.title}</h3>
                        </div>
                        <p className="card-description">{test.description}</p>
                    </div>
                ))}
            </div>
        </>
    );
};

export default GeneratedContentCard;
