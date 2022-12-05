# %%
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import chardet
from chardet.universaldetector import UniversalDetector
import pymannkendall as mk

# %%
inputfile = '../input/input.csv'

# %%
# 文字コードの判別
# https://zenn.dev/takedato/articles/c3a491546f8c58 
with open(inputfile, 'rb') as f:  
  detector = UniversalDetector()
  for line in f:
    detector.feed(line)
    if detector.done:
      break
  detector.close()
  result = detector.result
  code = result['encoding']
  print(code)

# %%
if code == 'utf-8':
    code = 'utf-8'
elif code == 'UTF-8-SIG':
    code = 'utf-8'
else:
    code = 'shift-jis'
print(code)

# df = pd.read_csv(inputfile, index_col=0)
df = pd.read_csv(inputfile, index_col=0, encoding=code)
# df = pd.read_csv(inputfile, index_col=0, encoding="UTF-8")
df

# %%
np.array(df.index)

# %%
indexls = df.columns
b = np.array(df.columns)
num = b.shape[0] # 要素数取得
num

# %%
columnsls = ["trend", "h", "p", "z", "Tau", "s", "var_s", "slope", "intercept","r","R2"]

# %%
# matplotlibの設定

plt.rcParams['font.size'] = 15
plt.rcParams['font.family']= 'sans-serif'
plt.rcParams['font.sans-serif'] = ['Arial']

plt.rcParams['xtick.direction'] = 'out'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.major.width'] = 1
plt.rcParams['ytick.major.width'] = 1
plt.rcParams['axes.linewidth'] = 1
plt.rcParams['axes.grid'] = False
plt.rcParams['grid.linestyle']='--'
plt.rcParams['grid.linewidth'] = 0.2

plt.rcParams["xtick.minor.visible"] = False # x軸副目盛り線を描くかどうか
plt.rcParams["ytick.minor.visible"] = True # y軸副目盛り線を描くかどうか
plt.rcParams["xtick.minor.size"] = 3.0      # x軸副目盛り線の長さ
plt.rcParams["ytick.minor.size"] = 2.0      # y軸副目盛り線の長さ
plt.rcParams["xtick.minor.width"] = 0.6     # x軸副目盛り線の線幅
plt.rcParams["ytick.minor.width"] = 0.6     # y軸副目盛り線の線幅

plt.rcParams["legend.markerscale"] = 2
plt.rcParams["legend.fancybox"] = False
plt.rcParams["legend.framealpha"] = 1
plt.rcParams["legend.edgecolor"] = 'black'

# %%
def graph1(i):
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)

    ax.hist(df.iloc[:,i], color='black', bins=30)
    ax.set_title(f'{df.columns[i]}', fontname ='MS Gothic')
    ax.set_xlabel('x')
    ax.set_ylabel('Frequency')
    fig.savefig(f'../result/jpg/histogram_{df.columns[i]}.jpg')
    fig.savefig(f'../result/png/histogram_{df.columns[i]}.png')
    fig.savefig(f'../result/svg/histogram_{df.columns[i]}.svg')
    fig.show()

# %%
df.iloc[:,5]

# %%
df_corr = df.iloc[:,5]
df_corr = df_corr.rename_axis('year').reset_index()
df_corr

# %%
df_corr.corr()

# %%
mk.original_test(df.iloc[:,5])

# %%
def graph2(i):
    #figure()でグラフを表示する領域をつくり，figというオブジェクトにする．
    fig = plt.figure(figsize=(6.4,6), dpi=120, facecolor='w')

    #add_subplot()でグラフを描画する領域を追加する．引数は行，列，場所
    ax1 = fig.add_subplot(1, 1, 1)

    ax1.set_position([0.1, 0.6, 0.8, 0.3]) #ax.set_position([枠の左辺, 枠の下辺, 枠の横幅, 枠の高さ])
    #plt.subplots_adjust(wspace=0.4, hspace=0.4)

    # ax1.plot(df.index, df.iloc[:,3], c='black')

    ax1.plot(df.index, df.iloc[:,i],color="black",linewidth=1,marker=".",markersize=8)
    sns.regplot(x=df.index, y=df.iloc[:,i],color="black",ci=95, ax=ax1, marker="None",line_kws={"linewidth": 1.5})
    ax1.set_title(f'{df.columns[i]}', fontname ='MS Gothic')
    # ax1.set_xlabel('x')
    ax1.set_ylabel('')
    fig.savefig(f'../result/jpg/transition_{df.columns[i]}.jpg')
    fig.savefig(f'../result/png/transition_{df.columns[i]}.png')
    fig.savefig(f'../result/svg/transition_{df.columns[i]}.svg')

# %%
def main():
    result = pd.DataFrame(np.zeros((num, 11)),
                        columns = columnsls,
                        index = indexls)

    for i in range(num):
        trend, h, p, z, Tau, s, var_s, slope, intercept = mk.original_test(df.iloc[:,i])
        df_corr = df.iloc[:,i]
        df_corr = df_corr.rename_axis('year').reset_index()
        r = (df_corr.corr()).iloc[0,1]
        r2 = r*r
        resultls = [trend, h, p, z, Tau, s, var_s, slope, intercept, r, r2]
        result.iloc[i,:] = resultls

        graph1(i)
        graph2(i)
    return(result)

# %%
df_result = main()
df_result

# %%
df_result.to_csv('../result/result.csv', encoding="shift jis")


