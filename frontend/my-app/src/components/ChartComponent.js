import React from 'react';
import { Line } from 'react-chartjs-2';

const ChartComponent = ({ data, options }) => {
  return (
    <div>
      <Line data={data} options={options} />
    </div>
  );
};

export default ChartComponent;
