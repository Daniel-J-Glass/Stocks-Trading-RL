import config

from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.techindicators import TechIndicators
from alpha_vantage.sectorperformance import SectorPerformances

import pandas as pd
import matplotlib.pyplot as plt

import pickle as pkl

def download_data(symbols,output_format,output_size):
    ts = TimeSeries(key=config.api_key,output_format=output_format)
    ti = TechIndicators(key=config.api_key, output_format=output_format)

    for symbol in symbols:
        data, meta_data = ts.get_intraday(symbol=symbol, interval = "15min",outputsize=output_size)
        print(meta_data)

        data.to_pickle("{information} {symbol} {interval} {output_size}.pkl".format(
                information = meta_data["1. Information"],
                symbol=meta_data["2. Symbol"], 
                interval = meta_data["4. Interval"], 
                output_size = meta_data["5. Output Size"]
                )
            )

        data, meta_data = ti.get_bbands(symbol=symbol, interval='15min', time_period=240,series_type="close")
        print(meta_data)

        data.to_pickle("{symbol} {indicator} {interval}.pkl".format(
                symbol = meta_data["1: Symbol"],
                indicator=meta_data["2: Indicator"], 
                interval = meta_data["4: Interval"]
                )
            )
    
def main():
    symbols = ["AAPL"]

    #retrieve data
    if do_pull_data:
        download_data(symbols=symbols,output_format="pandas",output_size="full")
    
    #loading df for vis
    df = pd.read_pickle("Intraday (15min) open, high, low, close prices and volume AAPL 15min Full size.pkl")

    print(df)
    df['4. close'].plot()
    print(len(df.index))
    # plt.title('Intraday Close MSFT 15min Compact')
    plt.grid()
    plt.show()


if __name__=='__main__':
    do_pull_data = False
    main()

    
