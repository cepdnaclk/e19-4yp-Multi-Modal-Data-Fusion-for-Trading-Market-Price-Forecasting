// src/components/Graph.jsx - path
import React, { useEffect, useState } from 'react'
import Papa from 'papaparse'
import ReactApexChart from 'react-apexcharts'

export default function Graph() {
  const [series, setSeries] = useState([])
  const [options, setOptions] = useState({
    chart: {
      type: 'line',
      height: 400,
      zoom: { enabled: true, autoScaleYaxis: true },
      toolbar: { show: true },
      animations: { enabled: false },
    },
    stroke: { curve: 'smooth', width: 2 },
    xaxis: {
      type: 'datetime',
      labels: { datetimeUTC: false },
      tooltip: { enabled: false },
    },
    yaxis: { tooltip: { enabled: false } },
    tooltip: { x: { format: 'dd MMM yyyy HH:mm' } },
    grid: { borderColor: '#eee' },
  })

  useEffect(() => {
    fetch('/historicalPriceData.csv')
      .then(r => {
        if (!r.ok) throw new Error(`CSV load failed: ${r.status}`)
        return r.text()
      })
      .then(csv => {
        const { data } = Papa.parse(csv, {
          header: true,
          dynamicTyping: true,
        })
        // transform into [[timestamp, price], ...]
        const pts = data
          .map(({ time, price }) => {
            const ms = new Date(time).getTime()
            return [ms, price]
          })
          .filter(([ms, price]) => !isNaN(ms) && typeof price === 'number')

        setSeries([
          {
            name: 'Price',
            data: pts,
          },
        ])
      })
      .catch(console.error)
  }, [])

  return (
    <div id="chart">
      <ReactApexChart
        options={options}
        series={series}
        type="line"
        height={400}
      />
    </div>
  )
}
