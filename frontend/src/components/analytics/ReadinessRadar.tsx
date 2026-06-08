import React from 'react';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts';

interface ReadinessScore {
  role_id: number;
  role_name: string;
  total_score: number;
}

export default function ReadinessRadar({ data }: { data: ReadinessScore[] }) {
  const chartData = data.map(item => ({
    subject: item.role_name,
    A: item.total_score,
    fullMark: 100,
  }));

  if (chartData.length === 0) return null;

  return (
    <div className="h-80 w-full">
      <ResponsiveContainer width="100%" height="100%">
        <RadarChart cx="50%" cy="50%" outerRadius="70%" data={chartData}>
          <PolarGrid stroke="#374151" />
          <PolarAngleAxis dataKey="subject" tick={{ fill: '#9ca3af', fontSize: 12 }} />
          <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} axisLine={false} />
          <Radar name="Readiness" dataKey="A" stroke="#14b8a6" fill="#14b8a6" fillOpacity={0.5} />
          <Tooltip 
            contentStyle={{ backgroundColor: '#111827', borderColor: '#374151', color: '#fff' }}
            itemStyle={{ color: '#14b8a6' }}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
}
