import sys
import numpy as np
import scipy.io.wavfile as sc
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import ffmpy as ff
import math as mt
import statistics as stats

# ourfile is a ndarray created by the scipy.io.wavfile.read method - this will be a server-side operation on each
# recorded snippet

def wav_analysis(ourfile):

    def sign_check(x, y):

        if x > 0 and y <= 0:

            return True

        elif x <= 0 and y > 0:

            return True

        else:

            return False

    def is_pause(gen_list, g1, g2):

        for m in gen_list[g1 + (int(ourfile[0] * 0.2)):g2 - (int(ourfile[0] * 0.2))]:

            if m > low_threshold:
                return False

        return True

    ourfile1 = ourfile[1].tolist()

    b = 0.5 * ourfile[0]

    r = 8 * ourfile[0]

    low_threshold = 2000

    peak_keep = 0

    peak_store = []

    peak_dict = {}

    curr_index = 0

    low_test = []

    for i in range(0, len(ourfile1), 1):

        if ourfile1[i] > 0:

            peak_store.append(ourfile1[i])

        if sign_check(ourfile1[i],peak_keep) and len(peak_store)>100:

            our_max = max(peak_store)

            try:
                indi = ourfile1[curr_index:i].index(our_max)

                peak_dict[indi + curr_index] = our_max

            except ValueError:
                pass

            curr_index = i

            peak_store = []

        peak_keep = ourfile1[i]

    avg = 3000

    filter_dict_volume = {}

    while(True):

        for k in peak_dict:
            if peak_dict[k] >= avg:
                filter_dict_volume[k] = peak_dict[k]

        if float(len(filter_dict_volume))>((len(ourfile1)/ourfile[0])*3):

            avg += 100
            filter_dict_volume = {}

        else:
            break

    sec = []

    up_down_pairs = []

    up_down = 0

    for h in range(0,len(ourfile1),1):

        sec.append(h)

        if ourfile1[h] > avg:

            low_test.append(0)

        else:

            low_test.append(ourfile1[h])

        if ourfile1[h]>avg and up_down == 0:

            up_down_pairs.append([sec[-1]])
            up_down = 1

        elif ourfile1[h]<avg and up_down == 1:

            up_down_pairs[-1].append(sec[-1])
            up_down = 0

    score_dict = {"Clarity":0, "Rhythmicity":0, "Emphasis/Tone":0}

    first_pause_g = 0
    first_wave_g = 0
    consec_pause_count = 0

    for g in range(1,len(up_down_pairs),1):

        # print(g)
        #print(prev_g)
        # print(float(g-prev_g))
        # print(b)
        # print(float(g-first_wave_g))
        # print(r)

        curr_g = up_down_pairs[g][0]

        prev_g = up_down_pairs[g-1][1]

        if consec_pause_count >= 5:
            #print("consec")
            score_dict["Rhythmicity"] -= 200

        if float(curr_g - prev_g) > b:

            if is_pause(low_test,prev_g,curr_g):
                #print("pause")
                consec_pause_count += 1
                score_dict["Rhythmicity"] += 100 #2.5 - ((g - prev_g)/ourfile[0])
                if consec_pause_count == 1:
                    first_pause_g = prev_g
            elif float(curr_g - prev_g) > 2*b:
                #print("elif")
                # print("this is your problem")
                score_dict["Clarity"] -= 1 #10/((len(ourfile1)/ourfile[0]))
                first_wave_g = g
            else:
                #print("else")
                score_dict["Clarity"] -= 0.5

        elif float(curr_g - first_wave_g) > r:
            #print("clear")
            score_dict["Clarity"] += 1 #10/((len(ourfile1)/ourfile[0]))
            consec_pause_count = 0

    final = []

    for n in filter_dict_volume:

        final.append(filter_dict_volume[n])

    stdevi = stats.stdev(final)

    score_dict["Emphasis/Tone"] = (stdevi/((max(final)-avg)))*100

    score_dict["Clarity"] = (score_dict["Clarity"]/(len(up_down_pairs)))*100

    score_dict["Rhythmicity"] = (score_dict["Rhythmicity"]/(len(up_down_pairs)))*100

    return score_dict
