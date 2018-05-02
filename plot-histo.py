import csv
import sys
import pandas as pd

import plotly as py
import plotly.graph_objs as go
from plotly.graph_objs import Scatter, Layout


def parse_data(filename):
    samples = None

    with open(filename) as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')

        header = next(reader)
        samples = header[6:]

        data = []
        non_zeros = []
        for row in reader:
            data.append(row[6:])
            for val in row[6:]:
                if val == '':
                    val = float(0)
                    data.append(val)
                else:
                    val = float(val)
                    non_zeros.append(val)
                    data.append(val)

    tsvfile.close()

    return [non_zeros, data, samples]


def generate_histo(non_zeros):
    trace2 = go.Histogram(x=non_zeros)
    data = [trace2]

    return data


def get_layout_attributes(plot_title, xlabel, ylabel):
    layout = go.Layout(
        title=plot_title,
        xaxis=dict(
            title=xlabel
        ),
        yaxis=dict(
            title=ylabel
        ),
        bargap=0.2,
        bargroupgap=0.1
    )

    return layout


def generate_heatmap(non_zeros, samples):

    trace = go.Heatmap(z=non_zeros,
                       x=samples,
                       y=samples, colorscale='Greys')
    data = [trace]

    return data



if __name__ == '__main__':

    print('Program to plot histogram of merged cnvs')

    parameters = sys.argv
    argc = len(parameters)
    if argc != 2:
        print("Usage: <input tsv file name>")
        sys.exit(0)

    non_zeros = []
    filename = sys.argv[1]
    # filename = 'mmr-fcctx-adjusted-merged-canon.tsv'
    outfilename = 'mmr_fcctx_snp_histo.html'

    plot_title = 'MMR and FCCTX merged-canonized'
    plot_xlabel = 'Confidence'
    plot_ylabel = 'Count'

    tempdata = parse_data(filename)
    non_zeros = tempdata[0]
    zeros = tempdata[1]
    samples = tempdata[2]

    data_histo = generate_histo(non_zeros)
    layout = get_layout_attributes(plot_title, plot_xlabel, plot_ylabel)

    data_heatmap = generate_heatmap(non_zeros, samples)

    fig = go.Figure(data=data_histo, layout=layout)

    # py.offline.plot(data, filename='plots/'+ 'fcctx_snp_similarity.html')
    py.offline.plot(fig, filename='plots/' + outfilename)
