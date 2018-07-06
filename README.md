# Pluton Cryptocurrency Trading Bot

## Screenshots
![Screenshot](https://github.com/clixx-io/pluton-cryptobot/raw/master/doc/images/2018-07-06-182650.png)

This bot is a fork of bwentzloff's project https://github.com/bwentzloff/trading-bot to
build a CryptoBot with Deep Statistical using Data Analysis Tools of Scientific Quality.

This is a Learning and Analysis tool and the current State is In-Development/Experimental. 

The characteristics that make this Bot different are:

 - Analyse Historical Data with Pandas Data Analysis (Scientific Standard) Tool
 
 - Mesh Overlays for predictive Buy/Sell/Hold Actions (in development)
 
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

| FrameWork  | Description                              |
| ---------- | ---------------------------------------- |
| Pandas     | Data Analytics Framework                 |
| Matplotlib | 2D plotting library for Graph Generation |
| cryptocmd  | Used to Download Historical Data         |
| cheetah    | Reporting and Html templating engine     |
| PyTables   | HDF5 format for Data Storage             |

Backtesting is supported using Cryptocmd. More backtesting and using other exchanges and live trading are planned.

Backtesting can be run using the following command:
`python backtest.py`

