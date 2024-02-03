# Adapted by Brian Green from code written by Doug Klink

from typing import List

import numpy as np
import matplotlib.pyplot as plt


def before_and_after_segments(segments_before, segments_after, nplots, var_diff, var):
    # Find segments that are different
    diff_segs = segments_before.copy()
    diff_segs[var_diff] = segments_after[var_diff]-segments_before[var_diff]
    diff_segs[var_diff] = diff_segs[var_diff]/diff_segs[var_diff]
    diff_segs = diff_segs.groupby('segment_id').apply(lambda f: f.sum(axis=0)).drop(columns=['segment_id'])
    segments_before = segments_before[~segments_before.segment_id.isin(diff_segs.index[(diff_segs[var_diff]==0.)])]
    segments_after = segments_after[~segments_after.segment_id.isin(diff_segs.index[(diff_segs[var_diff]==0.)])]
    for s_id in np.random.choice(segments_before.segment_id.unique(), nplots):
        before = segments_before[segments_before.segment_id == s_id]
        after = segments_after[segments_after.segment_id == s_id]
        nvals = diff_segs[diff_segs.index == s_id]
        nvals = nvals[var_diff].iloc[0]
        plt.figure(figsize=(10,3))
        plt.plot(before.time, before[var], label='before')
        plt.plot(after.time, after[var], label='after', alpha=.8)
        plt.gca().invert_yaxis()
        plt.ylabel(var)
        plt.title(f'segment {s_id}, number of changes: {nvals}')
        plt.legend()
        plt.xticks(rotation=30)
        
def before_and_after_flights(flights_before, flights_after, nplots, var_diff, var):
    # Find segments that are different
    diff_flts = flights_before.copy()
    diff_flts[var_diff] = flights_after[var_diff]-flights_before[var_diff]
    diff_flts[var_diff] = diff_flts[var_diff]/diff_flts[var_diff]
    diff_flts = diff_flts.groupby('flight_id').apply(lambda f: f.sum(axis=0)).drop(columns=['flight_id'])
    flights_before = flights_before[~flights_before.flight_id.isin(diff_flts.index[(diff_flts[var_diff]==0.)])]
    flights_after = flights_after[~flights_after.flight_id.isin(diff_flts.index[(diff_flts[var_diff]==0.)])]
    for f_id in np.random.choice(flights_before.flight_id.unique(), nplots):
        before = flights_before[flights_before.flight_id == f_id]
        after = flights_after[flights_after.flight_id == f_id]
        nvals = diff_flts[diff_flts.index == f_id]
        nvals = nvals[var_diff].iloc[0]
        plt.figure(figsize=(10,3))
        plt.plot(before.time, before[var], label='before')
        plt.plot(after.time, after[var], label='after', alpha=.8)
        plt.gca().invert_yaxis()
        plt.ylabel(var)
        plt.title(f'flight {f_id}, number of changes: {nvals}')
        plt.legend()
        plt.xticks(rotation=30)


def plot_every_flight(segments):
    """can use this to render plots of all flights.  If invoked from an ipython notebook with matplotlib set as
            inline (default behavior), it'll make the plots all the way down the page; you can quickly scroll through
            them all"""
    i = 0
    ids = segments.flight_id.unique()
    while i < len(ids):
        fig, ax = plt.subplots(3, 3, figsize=(10, 7))
        ax[0, 0].set_title('wind_u')
        ax[0, 1].set_title('wind_v')
        ax[0, 2].set_title('pressure')
        for j in range(3):
            fl = segments[segments.flight_id == ids[i]]
            ax[j, 0].plot(fl.time, fl.wind_u)
            ax[j, 0].set_xticks([])
            ax[j, 1].plot(fl.time, fl.wind_v)
            ax[j, 1].set_xticks([])
            ax[j, 2].plot(fl.time, fl.pressure/100)
            ax[j, 2].invert_yaxis()
            ax[j, 2].set_xticks([])
            ax[j, 0].set_ylabel(ids[i])
            i += 1
            if i == len(ids):
                break


def view_segments(segments, variables: List[str], group_col='segment_id'):
    """
    Plots requested variables for each segment, waiting for input before rendering next segment/flight
    :param segments: DataFrame of Loon data, e.g. anything in temp_data
    :param variables: subset of ['latitude', 'longitude', 'altitude', 'temperature', 'pressure', 'wind_u', 'wind_v']
    :param group_col: one of ['segment_id', 'flight_id']
    """

    print('enter to view next segment, q to terminate')
    for i, [f_id, flight] in enumerate(segments.groupby(group_col)):
        fig, ax = plt.subplots(len(variables), sharex='all', figsize=(9, 8))
        for j, y_var in enumerate(variables):
            ax[j].plot(flight.time, flight[y_var])
            ax[j].set_ylabel(y_var)
            if y_var == 'pressure':
                ax[j].invert_yaxis()
        ax[-1].set_xlabel('time')
        plt.xticks(rotation=30)
        plt.suptitle(f'{group_col}={f_id}, {i+1}/{len(segments)}')
        plt.pause(0.1)  # shows the figure.  matplotlib is weird

        response = input()
        while response not in ["", 'q']:
            response = input('invalid command')
        plt.close(fig)
        if response == 'q':
            break
