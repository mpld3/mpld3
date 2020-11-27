import matplotlib.pyplot as plt
import numpy as np
import mpld3


def create_plot():
    try:
        import pandas as pd
    except Exception:
        from nose import SkipTest
        raise SkipTest("pandas not installed")
    df2_index = pd.date_range(start="2010-01-01", periods=100, freq='D')
    df2 = pd.DataFrame({'a': range(100)}, index=df2_index)
    ax = df2.plot(title="Datetime DF")  # noqa
    return plt.gcf()


def test_pandas_timeaxis():
    fig = create_plot()
    _ = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
