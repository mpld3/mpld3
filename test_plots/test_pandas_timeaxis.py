import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def main():
    df2_index = pd.DatetimeIndex(start="2010-01-01", periods=100, freq='D')
    df2 = pd.DataFrame({'a':range(100)}, index=df2_index)
    ax = df2.plot(title="Datetime DF")

    return plt.gcf()


if __name__ == "__main__":
    main()
    plt.show()
