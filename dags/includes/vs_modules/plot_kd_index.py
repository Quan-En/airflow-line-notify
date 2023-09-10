
import matplotlib.pyplot as plt
import io
import pandas as pd
import pickle

# def plot_kd_index_2_buffer(df:pd.DataFrame, title:str=None) -> io.BytesIO:

#     fig = plt.figure()
#     ax = plt.axes()
#     ax.plot(df['K'], label='K')
#     ax.plot(df['D'], label='D')
#     plt.legend(loc='upper right', shadow=True, fontsize='x-large')
#     if title:
#         plt.title(title)
#     plt.xticks(rotation=45)
#     plt.ylim(0, 100)
    
#     buf = io.BytesIO()
#     # pickle.dump(fig, buf)
#     plt.savefig(buf, format='png')
#     buf.seek(0)

#     return buf

def plot_kd_index_2_file(df:pd.DataFrame, title:str=None) -> str:

    plt.plot(df['K'], label='K')
    plt.plot(df['D'], label='D')
    plt.legend(loc='upper right', shadow=True, fontsize='x-large')
    if title:
        plt.title(title)
    plt.xticks(rotation=45)
    plt.ylim(0, 100)

    plt.savefig("matplot.png")

    return "matplot.png"