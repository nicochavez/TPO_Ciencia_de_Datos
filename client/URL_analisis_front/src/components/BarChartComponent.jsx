import React from 'react';
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    Tooltip,
    Legend,
    ResponsiveContainer
} from 'recharts';

const BarChartComponent = ({ positive, negative }) => {
    const data = [
        { name: 'Resultados', Phishing: positive, Seguro: negative }
    ];

    return (
        <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data}>
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="Phishing" fill="#F44336" />
                <Bar dataKey="Seguro" fill="#4CAF50" />
            </BarChart>
        </ResponsiveContainer>
    );
};

export default BarChartComponent;
