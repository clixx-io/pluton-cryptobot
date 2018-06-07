# Pluton Cryptocurrency Trading Bot

This bot is a fork of bwentzloff's project https://github.com/bwentzloff/trading-bot to
build a CryptoCurrency Analysis and Trading Bot with an Analytical Side for past and future
probable data.

This is a Learning and Analysis tool and the current State is In-Development/Experimental. 

The characteristics that make this Bot different are:

 - Download and Analyse Historical Coin Data with the Powerful Pandas Data Analysis Tool
 
 - It supports Mesh Overlays for predictive Buy/Sell/Hold Actions (in development)
 
 - Produce HTML Reports that can be viewed on a Browser (coming soon)
 
 - Generate and React to Realtime signals with MQTT (coming soon)
 
 - Do predictive 'What if?' modelling such as incorporating RV data. (coming soon)
 
Mesh's are such things as Star Patterns, Moon Patterns, Paydays and Weekends
for predictive modelling. After all, we are all people and these things affect us and
our Buying and Selling Moods.

If you have a thought and wish to model in how Christmas Shopping may affect values
or some other future Event then this tool will allow you to make Projections and
Extrapolation Graphs using these Adjusters.

Libraries used on this Project include:

| FrameWork | Description                              |
| --------- | ---------------------------------------- |
| Pandas    | Data Analytics Framework                 |
| cryptocmd | Used to Download Historical Data         |

Backtesting is supported using Cryptocmd. More backtesting and using other exchanges and live trading are planned.

Backtesting can be run using the following command:
`python backtest.py`
