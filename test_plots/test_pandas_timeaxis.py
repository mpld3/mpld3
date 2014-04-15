import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mpld3

df2_index = pd.DatetimeIndex(start="2010-01-01", periods=100, freq='D')
df2 = pd.DataFrame({'a': range(100)}, index=df2_index)
ax = df2.plot(title="Datetime DF")

mpld3.show()
