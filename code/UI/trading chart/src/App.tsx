import React, { useEffect, useState } from 'react';
import CandlestickChart from './TradingChart';

interface CandlestickData {
    time: number;
    open: number;
    high: number;
    low: number;
    close: number;
}

export default function App() {
    const [candlestickData, setCandlestickData] = useState<CandlestickData[]>([]);

    useEffect(() => {
        async function fetchCandlestickData() {
            try {
                const response = await fetch(
                    'https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=500'
                );
                const data = await response.json();

                // Convert timestamps to readable format
                const formattedData: CandlestickData[] = data.map((item: any) => ({
                    time: item[0] / 1000, // Convert milliseconds to seconds
                    open: parseFloat(item[1]),
                    high: parseFloat(item[2]),
                    low: parseFloat(item[3]),
                    close: parseFloat(item[4]),
                }));

                setCandlestickData(formattedData);
            } catch (error) {
                console.error('Error fetching candlestick data:', error);
            }
        }

        fetchCandlestickData();
        const interval = setInterval(fetchCandlestickData, 60000); // Fetch every 60 seconds

        return () => clearInterval(interval);
    }, []);

    return (
        <div className="chart-container">
            <h1>BTC/USDT Candlestick Chart</h1>
            <CandlestickChart data={candlestickData} />
        </div>
    );
}
