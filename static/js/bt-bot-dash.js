// exchange-dashboard.js
document.addEventListener('DOMContentLoaded', function () {
    const refreshButton = document.getElementById('refresh-data');

    if (refreshButton) {
        refreshButton.addEventListener('click', fetchLatestData);

        // Auto refresh every 30 seconds
        setInterval(fetchLatestData, 30000);
    }

    // Add custom template filters equivalent
    function multiply(a, b) {
        return parseFloat(a) * parseFloat(b);
    }

    function subtract(a, b) {
        return parseFloat(a) - parseFloat(b);
    }

    function divide(a, b) {
        return b !== 0 ? parseFloat(a) / parseFloat(b) : 0;
    }

    function formatNumber(num, decimals = 2) {
        return parseFloat(num).toFixed(decimals);
    }

    function fetchLatestData() {
        // Show loading indicator
        refreshButton.textContent = 'Loading...';
        refreshButton.disabled = true;

        fetch('/standalone-apps/exchange-data-api/')
            .then(response => response.json())
            .then(data => {
                // Update rates
                document.getElementById('usd-zar').textContent = data.usd_zar;
                document.getElementById('binance-btc-usdt').textContent = data.binance_btc_usdt;
                document.getElementById('valr-btc-zar').textContent = data.valr_btc_zar;

                // Update LGP
                const binanceValrLgp = document.getElementById('binance-valr-lgp');
                binanceValrLgp.textContent = data.binance_to_valr_lgp + '%';
                binanceValrLgp.parentElement.className = `lgp-item ${data.binance_to_valr_lgp > 0 ? 'positive' : data.binance_to_valr_lgp < 0 ? 'negative' : ''}`;

                const valrBinanceLgp = document.getElementById('valr-binance-lgp');
                valrBinanceLgp.textContent = data.valr_to_binance_lgp + '%';
                valrBinanceLgp.parentElement.className = `lgp-item ${data.valr_to_binance_lgp > 0 ? 'positive' : data.valr_to_binance_lgp < 0 ? 'negative' : ''}`;

                // Update trade recommendation
                const tradeRecommendation = document.getElementById('trade-recommendation');

                if (data.lgp_result && data.lgp_result.action) {
                    tradeRecommendation.innerHTML = `
                        <div class="trade-action">${data.lgp_result.action}</div>
                        <div class="trade-explanation">${data.lgp_result.explanation}</div>
                        ${data.lgp_result.estimated_profit ? `<div class="trade-profit">Est. Profit: ${data.lgp_result.estimated_profit}</div>` : ''}
                    `;
                } else {
                    tradeRecommendation.innerHTML = `<div class="trade-action">No profitable arbitrage opportunity at this time</div>`;
                }

                // Update order books
                updateOrderBook('valr-asks', data.valr_asks);
                updateOrderBook('valr-bids', data.valr_bids);

                // Update Binance order books with ZAR conversion
                updateOrderBook('binance-asks', data.binance_asks_zar, true);
                updateOrderBook('binance-bids', data.binance_bids_zar, true);

                // Update spreads
                if (data.valr_asks && data.valr_asks.length > 0 && data.valr_bids && data.valr_bids.length > 0) {
                    const valrAskPrice = parseFloat(data.valr_asks[0][0]);
                    const valrBidPrice = parseFloat(data.valr_bids[0][0]);
                    const valrSpread = valrAskPrice - valrBidPrice;
                    const valrSpreadPercent = (valrSpread / valrBidPrice) * 100;

                    document.getElementById('valr-spread').innerHTML = `
                        <div class="spread-label">Spread:</div>
                        <div class="spread-value">${formatNumber(valrSpread)} ZAR (${formatNumber(valrSpreadPercent)}%)</div>
                    `;
                }

                if (data.binance_asks_zar && data.binance_asks_zar.length > 0 && data.binance_bids_zar && data.binance_bids_zar.length > 0) {
                    const binanceAskPrice = parseFloat(data.binance_asks_zar[0][0]);
                    const binanceBidPrice = parseFloat(data.binance_bids_zar[0][0]);
                    const binanceSpread = binanceAskPrice - binanceBidPrice;
                    const binanceSpreadPercent = (binanceSpread / binanceBidPrice) * 100;

                    document.getElementById('binance-spread').innerHTML = `
                        <div class="spread-label">Spread:</div>
                        <div class="spread-value">${formatNumber(binanceSpread)} ZAR (${formatNumber(binanceSpreadPercent)}%)</div>
                    `;
                }

                // Update timestamp
                document.getElementById('timestamp').textContent = data.timestamp;

                // Reset button
                refreshButton.textContent = 'Refresh';
                refreshButton.disabled = false;
            })
            .catch(error => {
                console.error('Error fetching data:', error);
                refreshButton.textContent = 'Refresh (Failed)';
                refreshButton.disabled = false;

                // Try again after 5 seconds
                setTimeout(() => {
                    refreshButton.textContent = 'Refresh';
                }, 5000);
            });
    }

    function updateOrderBook(elementId, data, isZarConverted = false) {
        const container = document.getElementById(elementId);
        if (!container || !data) return;

        let html = '';

        data.forEach(item => {
            const price = isZarConverted ? parseFloat(item[0]) : parseFloat(item[0]);
            const amount = parseFloat(item[1]);
            const total = price * amount;

            html += `
                <div class="book-row">
                    <div class="col price">${formatNumber(price)}</div>
                    <div class="col amount">${formatNumber(amount, 8)}</div>
                    <div class="col total">${formatNumber(total)}</div>
                </div>
            `;
        });

        container.innerHTML = html;
    }
});