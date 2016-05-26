"""Plot to test line with drawstyle steps"""
import matplotlib.pyplot as plt
import mpld3


def create_plot():
    fig, ax = plt.subplots()

    x = [0, 1]

    ax.plot(range(5),range(9,4,-1),drawstyle='steps', marker='*')
    ax.plot(range(5),range(5,0,-1),drawstyle='steps-post', marker='*')
    ax.plot(range(5),range(7,2,-1),drawstyle='steps-mid', marker='*')
    
    ax.set_ylim(0, 10)
    ax.set_xlim(0, 5)
    ax.set_title("Line with drawstyle steps", size=20)
    
    return fig


def test_lines_with_steps():
    fig = create_plot()
    html = mpld3.fig_to_html(fig)
    plt.close(fig)


if __name__ == "__main__":
    mpld3.show(create_plot())
