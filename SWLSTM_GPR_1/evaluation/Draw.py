# -*- coding: utf-8 -*-
# @File         : Draw.py
# @Author       : Zhendong Zhang
# @Email        : zzd_zzd@hust.edu.cn
# @University   : Huazhong University of Science and Technology
# @Date         : 2019/7/31
# @Software     : PyCharm
# -*---------------------------------------------------------*-

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from statsmodels.graphics.api import qqplot
plt.rc('font', family='Times New Roman')


class DrawUtils(object):

    # draw prediction results
    def drawPredictions(self, predictions, observations, lower, upper, alpha,
                        isInterval, xlabel, ylabel, title, legendLoc, isSave, savePath, isShow):
        lw = 2
        fontsize = 20
        index = [i for i in range(observations.shape[0])]

        fig, axs = plt.subplots(1, 1, figsize=(12, 6))

        axs.plot(index, observations, marker="o", markersize=3, label="observations", lw=lw, color='r')#(1, 0.38824, 0.27843)
        preColor = (0.11765,	0.56471,	1)
        axs.plot(index, predictions, marker="D", markersize=3, label="predictions", lw=lw, color=preColor)
        if isInterval:
            axs.plot(index, lower, color=preColor, lw=lw/2)
            axs.plot(index, upper, color=preColor, lw=lw/2)
            axs.fill_between(index, lower, upper, alpha=1, color=(0.9, 0.9, 0.9), label=''+alpha+' prediction interval')
            for i in range(len(index)):
                if observations[i] > upper[i] or observations[i] < lower[i]:
                    axs.plot(index[i], observations[i], marker="o", markersize=3, color='chartreuse')

        residual = observations-predictions
        axs2 = axs.twinx()
        axs2.bar(index, residual, fc='grey', label='residual error')
        axs2.set_ylabel("residual error(m/s)", fontsize=fontsize)
        axs2.set_ylim([round(min(residual)*11), round(max(residual)*1.6)])

        ymajorLocator2 = MultipleLocator(4.0)
        axs2.yaxis.set_major_locator(ymajorLocator2)
        axs.grid()

        xmajorLocator = MultipleLocator(10)
        xminorLocator = MultipleLocator(5)
        ymajorLocator = MultipleLocator(2.0)
        yminorLocator = MultipleLocator(1.0)

        axs.xaxis.set_major_locator(xmajorLocator)
        axs.yaxis.set_major_locator(ymajorLocator)

        axs.xaxis.set_minor_locator(xminorLocator)
        axs.yaxis.set_minor_locator(yminorLocator)

        axs.xaxis.grid(True, which='major')
        axs.yaxis.grid(True, which='minor')

        axs.set_title(title, loc="center", fontsize=fontsize)
        axs.set_xlim([min(index), max(index)])
        if isInterval:
            axs.set_ylim([0.0, round(max(upper)*1.2)])
        else:
            axs.set_ylim([0.0, round(max(max(predictions), max(observations)) * 1.2)])
        axs.set_xlabel(xlabel, fontsize=fontsize)
        axs.set_ylabel(ylabel, fontsize=fontsize)
        plt.xticks(fontsize=fontsize)
        if max(residual) > 6:
            plt.yticks(np.array([-4, 0, 4, 8]), fontsize=15)
        else:
            plt.yticks(np.array([-4, 0, 4]), fontsize=15)

        fig.legend(fontsize=fontsize-5, bbox_to_anchor=legendLoc, bbox_transform=axs.transAxes)
        plt.tight_layout()
        if isShow:
            plt.show()
        if isSave:
            fig.savefig(savePath, bbox_inches="tight", dpi=300)
        plt.close()

    # check for reliability
    def drawPIT(self, data, cdf, xlabel, ylabel, title, isSave, savePath, isShow):
        lw = 4
        fontsize = 40
        fig = plt.figure(figsize=(12, 12))
        axs = fig.add_subplot(111)
        fig = qqplot(data, dist=cdf, line='45', ax=axs)
        deta = 1.358/(len(data))**0.5*(2**0.5)
        axs.plot([deta, 1], [0, 1-deta], '--', color='blueviolet', lw=lw, label='Kolmogorov 5% significance band')
        axs.plot([0, 1-deta], [deta, 1], '--', color='blueviolet', lw=lw)
        axs.set_title(title, loc="center", fontsize=fontsize)
        axs.set_xlabel(xlabel, fontsize=fontsize)
        axs.set_ylabel(ylabel, fontsize=fontsize)
        axs.set_xlim([0, 1])
        axs.set_ylim([0, 1])
        plt.xticks(fontsize=fontsize)
        plt.yticks(fontsize=fontsize)
        plt.grid()
        plt.legend(fontsize=25)
        if isShow:
            plt.show()
        if isSave:
            fig.savefig(savePath, bbox_inches="tight", dpi=300)
        plt.close()
