import React from 'react';
import {
    PieChart,
    Pie,
    Cell,
    Tooltip,
    Legend,
    ResponsiveContainer
} from 'recharts';

const PieChartComponent = ({ positive, negative }) => {
    const data = [
        { name: 'Phishing', value: positive },
        { name: 'Seguro', value: negative }
    ];

    // Define colores para cada parte del gráfico
    const COLORS = ['#F44336', '#4CAF50'];

    return (
        <ResponsiveContainer width="100%" height={300}>
            <PieChart>
                <Pie
                    data={data}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                >
                    {data.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index]} />
                    ))}
                </Pie>
                <Tooltip />
                <Legend />
            </PieChart>
        </ResponsiveContainer>
    );
};

export default PieChartComponent;
