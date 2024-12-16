import pickle
import pandas as pd
import numpy as np
from statistics import mean, stdev
from scipy.fft import fft, fftfreq
from scipy.signal import butter, filtfilt, argrelextrema
import matplotlib.pyplot as plt
import Settings as s
import datetime


def repetition_features(data, hand, framepersec):
    data_maxmin = max_min(data)
    data_repDF = repetition_divison(data_maxmin[0], data_maxmin[1])
    frames_up_list = []  # The amount of frames in raising (up)
    frames_down_list = []  # The amount of frames in descent (down)
    start_values = []  # The angle value at the beginning of the repetition
    peak_values = []  # The angle value at the peak of the repetition (before decreasing)
    end_values = []  # The angle value at the end of the repetition
    vel_features_up = []  # The velocity and acceleration mean and sd values in raising
    vel_features_down = []  # The velocity and acceleration mean and sd values in descent
    for row in range(0, len(data_repDF)):
        rep_temp = data_repDF.iloc[row]
        peak_values.append(data[int(rep_temp[2])])
        try:
            start_values.append(data[int(rep_temp[1])])
        except ValueError:
            start_values.append(float("Nan"))
        try:
            end_values.append(data[int(rep_temp[3])])
        except ValueError:
            end_values.append(float("Nan"))
        frames_up = rep_temp[2] - rep_temp[1]  # Peak - Start
        frames_up_list.append(frames_up)
        frames_down = rep_temp[3] - rep_temp[2]  # End - Peak
        frames_down_list.append(frames_down)
        try:
            vel_features_up.append(vel_features(data[int(rep_temp[1]):int(rep_temp[2])], framepersec))
        except ValueError:
            vel_features_up.append([float("Nan") * 4])
        try:
            vel_features_down.append(vel_features(data[int(rep_temp[2]):int(rep_temp[3])], framepersec))
        except ValueError:
            vel_features_down.append([float("Nan") * 4])

    data_repDF["start_value"] = start_values
    data_repDF["peak_value"] = peak_values
    data_repDF["end_value"] = end_values
    data_repDF["num_frames_up"] = frames_up_list
    data_repDF["num_frames_down"] = frames_down_list
    data_repDF.insert(0, "hand", [hand] * len(data_repDF))
    veldf_down = pd.DataFrame(vel_features_down, columns=['vel_mean_down', 'vel_sd_down',
                                                          'acc_mean_down', 'acc_sd_down'])
    veldf_up = pd.DataFrame(vel_features_up, columns=['vel_mean_up', 'vel_sd_up', 'acc_mean_up', 'acc_sd_up'])
    data_repDF = pd.concat([data_repDF, veldf_down, veldf_up], axis=1)

    return data_repDF


def max_min(data):
    # return array of index(frame) local max and min after removing maximum values are greater than mean max
    # and minimum values that are lower than the mean minima
    max_index = argrelextrema(np.asarray(data), np.greater_equal)
    max_index = max_index[0]  # indexs of max_index
    last = max_index[-1]  # add last max since the repetition can finish with lower value than mean
    max_index = max_index[data[max_index] > mean(data)]
    max_index = np.append(max_index, last)
    min_index = argrelextrema(np.asarray(data), np.less_equal)
    min_index = min_index[0]  # indexs of min_index
    min_index = min_index[data[min_index] < mean(data)]
    return max_index, min_index


def repetition_divison(max_indx, min_indx):
    """
    :param max_indx - np array of times (index) of local max
    :param min_indx - np array of times (index) of local min
    :return df of repetition : {repetition number, start ind, peak ind, end ind}
    """
    done = False
    rep_count = 0
    iter_maxindx = 0
    iter_minindx = 0
    repetition = []

    while iter_maxindx < len(max_indx) and iter_minindx < len(min_indx):
        # rep_ind = []
        while max_indx[iter_maxindx] > min_indx[iter_minindx]:
            iter_minindx += 1
            if iter_minindx >= len(min_indx):
                done = True
                break
        rep_count += 1
        if iter_minindx-1 < 0:  # The motion starts without local minimum
            rep_ind = [rep_count, float("Nan"), max_indx[iter_maxindx]]
            # print(rep_count, " rep - start in:", 0, " peak in:", max_indx[iter_maxindx], end=" ")
        else:
            rep_ind = [rep_count, min_indx[iter_minindx-1], max_indx[iter_maxindx]]
            # print(rep_count, " rep-start in:", min_indx[iter_minindx-1], " peak in:", max_indx[iter_maxindx], end=" ")
        if done:
            repetition.append(rep_ind)
            # print('\n')
            break
        while max_indx[iter_maxindx] < min_indx[iter_minindx]:
            iter_maxindx += 1
            if iter_maxindx >= len(max_indx):
                break
        # print("finish in:", min_indx[iter_minindx])
        rep_ind.append(min_indx[iter_minindx])
        repetition.append(rep_ind)
    cols_name = ['rep', 'start_frame', 'peak_frame', 'end_frame']
    df_rep = pd.DataFrame(repetition, columns=cols_name)
    return df_rep


def vel_acc_calc(data, fps):
    # Input: np array of data
    # Output: velocity, acceleration, time array.
    N = len(data)
    time = np.linspace(0, N/fps, N)
    vel = np.diff(data)
    delta_t = time[1]-time[0]
    vel = vel/delta_t
    acc = np.diff(vel)/delta_t
    return vel, acc, time


def vel_features(data, fps):
    # return features of velocity after filtering data by buterworth filter 2nd degree with 6
    if len(data) <= 3:
        mean_sd = [float("Nan")]*4
    else:
        vel, acc, time = vel_acc_calc(data, fps)
        mean_sd = [mean(vel), stdev(vel), mean(acc), stdev(acc)]
    return mean_sd


def fft_function(data, fps):
    N = len(data)
    T = 1/fps
    yf = fft(data)
    yf = 2.0/N * np.abs(yf[0:N//2])
    xf = fftfreq(N, T)[:N//2]
    # plt.plot(xf[1:], yf[1:])
    return yf, xf


def fft_features(data, fps):
    """
    input: data, frame per second rate
    Perfom fft on data
    output: 3 DF (freq & mag) - frequencies with the highet magnitude
    """

    magnitude, frequency = fft_function(data, fps)
    # Reomve the DC, index 0 - frequency 0hz
    magnitude = magnitude[1:]
    frequency = frequency[1:]
    freq_num = len(frequency)
    mean_mag = mean(magnitude)
    sd_mag = stdev(magnitude)
    features = [freq_num, mean_mag, sd_mag]

    # 3 DF (with max magnitude)
    DF_ind = np.argpartition(magnitude, -3)[-3:]
    DF_ind = DF_ind[np.argsort(magnitude[DF_ind])]  # sort top 3 DF by magnitude
    DF_mag = magnitude[DF_ind]
    DF_freq = frequency[DF_ind]
    features = np.append(features, [DF_freq, DF_mag])

    # Cycle length and number of cycles, calculated by the main DF (which is the last element in the narray)
    CL = fps/DF_freq[2]  # Cycle length- seconds per cycle = 1/DF ; frames per cycle = fps*(1/DF)
    n = len(data)/CL  # number of cycles
    features = np.append(features, [CL, n])

    # df_cl_plot(data, frequency, magnitude, DF_freq, DF_mag, CL)
    return features


def fft_features_df(right_data, left_data, fps):
    right_fft = fft_features(right_data, fps)
    left_fft = fft_features(left_data, fps)

    col_name = ["freq num", "magnitude mean", "magnitude sd", "DF3_freq", "DF2_freq", "DF1_freq", "DF3_mag", "DF2_mag",
                "DF1_mag", "CL", "cycles num"]
    df = pd.DataFrame([right_fft, left_fft], columns=col_name)
    df.insert(0, "hand", ["right", "left"])
    return df


def feature_extraction(right, left):
    # Settings
    fps = 30  # frame per seconds of Nuitrack
    # For filtering
    cutoff_freq = 6
    filter_order = 2
    y, x = butter(filter_order, cutoff_freq/(fps/2))

    right = filtfilt(y, x, right)
    left = filtfilt(y, x, left)

    right_repDF = repetition_features(right, 'right', fps)
    left_repDF = repetition_features(left, 'left', fps)
    vel_df = pd.concat([right_repDF, left_repDF])

    fft_df = fft_features_df(right, left, fps)

    # Combine repetitions vel and acc features
    vel_df = vel_df.dropna()  # Drop rows with NA - so aggregate values won't be affect
    col_names = vel_df.columns[5:]  # columns to aggregate mean
    # defining the columns' aggregation functions
    col_dict = {'rep': 'count'}
    for c in col_names:
        col_dict[c] = ['mean', 'std']
    vel_df_grouped = vel_df.groupby(['hand']).agg(col_dict).reset_index()
    vel_df_grouped.columns = vel_df_grouped.columns.map('_'.join).str.strip('_')

    features = pd.merge(vel_df_grouped, fft_df, on=["hand"])
    return features


def predict_performance(features, exercise_name, model_name):
    model = pickle.load(open(f'{model_name}.sav', 'rb'))
    d_standardize_values = pickle.load(open('standardize_values_dict', 'rb'))

    if exercise_name not in d_standardize_values: # if exercise is not part of the model..
        exercise_name = 'raise_arms_bend_elbows'
    means = d_standardize_values[exercise_name]['means']
    std = d_standardize_values[exercise_name]['std']

    features_scaled = features
    features_scaled = features_scaled.iloc[:, 1:39] - pd.to_numeric(means)
    features_scaled = features_scaled / pd.to_numeric(std)

    model_features = model.model.data.xnames
    X_test = features_scaled[model_features]
    predictions = model.predict(X_test)
    print(predictions)
    # predictions = list(map(round, predictions))
    # print(predictions)
    return predictions


def plot_data(exercise_name, right_hand_data, left_hand_data):
    plt.figure()
    plt.plot(right_hand_data, label="right hand")
    plt.legend(loc='lower right')
    plt.plot(left_hand_data, label="left hand")
    plt.xlabel("Frame")
    plt.ylabel("Angle Degree")
    current_time = datetime.datetime.now()
    plt.savefig(s.participant_code+exercise_name+str(current_time.minute) + str(current_time.second)+'.png')
    # plt.show()


if __name__ == "__main__":

    path = r'C:\Users\mayak\PycharmProjects\DataAnalysis\CSV\Raw Data\maya_bend_elbows.csv'
    df = pd.read_csv(path)
    exercise = 'bend_elbows'
    adaptation_model_name = 'model2'
    for i in range(0,30,2):

        DATA_R = df.iloc[i]
        name = DATA_R[0]
        DATA_R = DATA_R[2:].dropna().to_numpy()
        DATA_L = df.iloc[i+1]
        DATA_L = DATA_L[2:].dropna().to_numpy()
        print(name)
        features = feature_extraction(DATA_R, DATA_L)
        predict_performance(features, exercise, adaptation_model_name)

    # exercise_names = ['raise_arms_horizontally', 'bend_elbows', 'raise_arms_bend_elbows']


    adaptation_model_name = 'model2'
    adaptation_model = pickle.load(open(f'{adaptation_model_name}.sav', 'rb'))

    model_features = adaptation_model.model.data.xnames
    X_test = features[model_features]
    predictions = adaptation_model.predict(X_test)
    print(predictions)
