# 2次元の AGI

import numpy as np
from scipy import optimize as opt
from tkinter import *
from functools import partial

class AGI:
    def __init__(self, H, W, ld):
        #  initialize（画像処理関係）
        self.WIDTH = W
        self.HEIGHT = H  # window's width and height
        self.width = W * 0.9
        self.height = H * 0.9  # canvas's width and height
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
        self.arr_init = np.array([1, 0, 0, 0, 1, 0, 1, 1])
        self.lam_f = lambda x_pre,y_pre,x_new,y_new,p_norm,a1,b1,c1,a2,b2,c2,t,s: \
           ((s*(a2 + c2*x_pre) + t*(b2 + c2*y_pre - 1))**2 + (s*(a1 + c1*x_pre - 1) + t*(b1 + c1*y_pre))**2 +
           (s**2 + t**2 - 1)**2 + (a1*x_pre + b1*y_pre + c1*p_norm - x_new)**2 +
           (a2*x_pre + b2*y_pre + c2*p_norm - y_new)**2 +
           (a1*a2 + b1*b2 + c1*c2*p_norm + x_pre*(a1*c2 + a2*c1) + y_pre*(b1*c2 + b2*c1))**2 +
           (a1**2 + 2*a1*c1*x_pre + b1**2 + 2*b1*c1*y_pre + c1**2*p_norm - 1)**2 +
           (a2**2 + 2*a2*c2*x_pre + b2**2 + 2*b2*c2*y_pre + c2**2*p_norm - 1)**2)
        self.update_points()

    # Calculation Space (C) : 射影更新時の計算における実際の座標系
    # Drawing Space (D) : tkinter の描画における画面の座標系
    # transfer 'Calculation Space' to 'Drawing Space'
    def c2d(self, pnt, bool):  # データの座標を射影する平面の画面サイズに合わせる
        if (bool):
            return self.width * (pnt + self.boundingH / 2) / self.boundingH + (self.WIDTH - self.width) / 2
        else:
            return (self.height - 100) * (self.boundingV / 2 - pnt) / self.boundingV + (self.HEIGHT - self.height) / 2

    def d2c(self,pnt, bool):  # 射影された平面上の座標を元のスケールに戻す
        if (bool):
            return self.boundingH * ((pnt - (self.WIDTH - self.width) / 2) - self.width / 2) / self.width
        else:
            return self.boundingV * ((pnt - (self.HEIGHT - self.height) / 2) - (self.height - 100) / 2) / (100 - self.height)

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
            self.Pos_scaled[0, i] = self.c2d(self.Pos_origin[i, 0], True)
            self.Pos_scaled[1, i] = self.c2d(self.Pos_origin[i, 1], False)

    def node_update(self, pos_newX, pos_newY, thisID):
        x2 = self.d2c(pos_newX, True)
        y2 = self.d2c(pos_newY, False)
        p_p = self.HighDimSpace[thisID].dot(self.HighDimSpace[thisID])
        self.Es[:, 2] = self.HighDimSpace[thisID]
        f2 = partial(self.lam_f, self.Pos_origin[thisID, 0], self.Pos_origin[thisID, 1], x2, y2, p_p)
        def g(args): return f2(*args)

        res = opt.minimize(g, self.arr_init, method='L-BFGS-B')
        if (res.success):
            Coefficient = res.x[0:6].reshape(2, 3)
            print(Coefficient)
            self.Es[:, 0:2] = self.Es.dot(Coefficient.T)
            self.update_points()
