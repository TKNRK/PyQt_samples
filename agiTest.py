# 2次元の AGI

import numpy as np
from scipy import optimize as opt
from tkinter import *
from functools import partial

class AGI:
    def __init__(self, B, b, ld):
        #  initialize（画像処理関係）
        self.WIDTH = self.HEIGHT = B  # window's width and height
        self.width = self.height = b  # canvas's width and height
        # initialize(データ処理関係)
        # load adjacency and multi-dimensional space
        self.EdgeList = np.genfromtxt('csv/edgeList.csv', delimiter=",").astype(np.int64) - 1
        self.edge_num = len(self.EdgeList)
        self.HighDimSpace = np.genfromtxt('csv/mdSpace.csv', delimiter=",")
        self.node_num, self.high_dim = self.HighDimSpace.shape
        self.low_dim = ld  # この次元のAGIを実行する
        self.Es = self.genE()  # 射影ベクトルを縦ベクトルで格納(low_dim行が射影ベクトルで、もう１行がベクトル)
        self.Pos_origin = None  # 計算するデータの実際の座標
        self.Pos_scaled = np.zeros(self.node_num * self.low_dim).reshape(self.low_dim, self.node_num)  # 画面サイズに合わせたデータの座標
        self.boundingV = 0  # Vertical boundary
        self.boundingH = 0  # Horizontal boundary
        self.update_points()

    # Calculation Space (C) : 射影更新時の計算における実際の座標系
    # Drawing Space (D) : tkinter の描画における画面の座標系
    # transfer 'Calculation Space' to 'Drawing Space'
    def c2d(self, pnt, bool):  # データの座標を射影する平面の画面サイズに合わせる
        if (bool):
            return self.width * (pnt + self.boundingH / 2) / self.boundingH + (self.WIDTH - self.width) / 2
        else:
            return (self.height - 100) * (self.boundingV / 2 - pnt) / self.boundingV + (self.HEIGHT - self.height) / 2

    # generate projection vectors
    def genE(self):
        L = np.diag(np.sqrt(np.genfromtxt('csv/eigVals.csv', delimiter=",")[0:self.high_dim]))
        base = np.zeros(self.high_dim * self.low_dim).reshape(self.high_dim, self.low_dim)
        for i in range(self.high_dim): base[i][i % self.low_dim] = 1
        e0_column = np.zeros(self.high_dim).reshape(self.high_dim, 1)
        E = np.c_[L.dot(base), e0_column]
        return E  # 縦ベクトル

    def update_points(self):
        self.Pos_origin = self.HighDimSpace.dot(self.Es[:, 0:self.low_dim])
        self.boundingH = max([np.amax(self.Pos_origin[:, 0]), abs(np.amin(self.Pos_origin[:, 0]))]) * 2
        self.boundingV = max([np.amax(self.Pos_origin[:, 1]), abs(np.amin(self.Pos_origin[:, 1]))]) * 2
        for i in range(self.node_num):
            self.Pos_scaled[0, i] = self.c2d(self.Pos_origin[i, 0], True);
            self.Pos_scaled[1, i] = self.c2d(self.Pos_origin[i, 1], False)