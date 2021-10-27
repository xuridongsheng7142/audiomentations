import matplotlib.pyplot as plt


def plot_waveforms(wf1, wf2=None, wf3=None, title="Untitled"):
    """Plot one, two or three short 1D waveforms. Useful for debugging."""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(title)
    plt.plot(wf1, label="wf1", alpha=0.66)
    if wf2 is not None:
        plt.plot(wf2, label="wf2", alpha=0.66)
    if wf3 is not None:
        plt.plot(wf3, label="wf3", alpha=0.66)
    plt.legend()
    plt.show()
    plt.close(fig)


def plot_matrix(matrix, output_image_path=None, vmin=None, vmax=None, title=None):
    """
    Plot a 2D matrix with viridis color map

    :param matrix: 2D numpy array
    :return:
    """
    fig = plt.figure()
    ax = fig.add_subplot(111)
    if title is not None:
        ax.set_title(title)
    plt.imshow(matrix, vmin=vmin, vmax=vmax, aspect="auto")
    plt.colorbar()
    if output_image_path:
        plt.savefig(str(output_image_path), dpi=200)
    else:
        plt.show()
    plt.close(fig)


def plot_waveform_and_spectrogram(
    samples, sample_rate, title="", output_file_path=None
):
    fig, axs = plt.subplots(2)
    fig.suptitle(title)

    # 1st
    axs[0].plot(x, y)
    # 2nd
    axs[1].plot(x, -y)

    if output_file_path is None:
        plt.show()
    else:
        pass  # TODO: Write to file
    plt.close(fig)
