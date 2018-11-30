import numpy as np
import numexpr as ne

class KernelRidgeRegression:
    def __init__(self, type="linear", lambd=1, c1=1, c2=1, d=1):
        self.type = type
        self.lambd = lambd
        self.c1 = c1
        self.c2 = c2
        self.d = d
        self.weigths = []
        self.fitted = False

    def _subt(self, A, B):
        A_3D = A[:, np.newaxis]
        return ne.evaluate('A_3D - B')
    #Linear
    def _linear(self, A, B, c, *args):
        return np.tensordot(A,B,axes=([1],[1]))+c

    #Polynomial
    def _poly(self, A, B, c1, c2, d, *args):
        return np.power(c1*np.tensordot(A,B,axes=([1],[1]))+c2,d)

    #Gaussian
    def _gauss(self, A, B, sigma, *args):
        return np.exp(   -np.square(np.linalg.norm(self._subt(A,B), axis=2)) / (2*(sigma**2))    )

    #Laplacian
    def _laplace(self, A, B, sigma, *args):
        return np.exp(   -(np.linalg.norm(self._subt(A,B), axis=2)) /  sigma    )

    def set_var(self, lambd=1, c1=1, c2=1, d=1):
        self.lambd = lambd
        self.c1 = c1
        self.c2 = c2
        self.d = d
        self.fitted = False
    def set_type(self, type):
        if type in ["linear","laplace","gauss","poly"]:
            self.type=type
        else:
            self.type="linear"
            print("Illegal type assignment, note allowed types are linear, \
                laplace, gauss, poly, defaulting to linear model")
        self.fitted = False
    def fit(self, X, Y):
        if (self.fitted == False):
            self.X = X
            self.Y = Y
            K = eval('self._'+self.type+'(self.X, self.X, self.c1, self.c2, self.d)')
            I = np.identity(len(X))
            self.weights = np.linalg.inv(np.matrix(K+self.lambd*I))
            self.fitted = True
        else:
            print("already fitted")
    def predict(self, Xp):
        if (self.fitted == False):
            print("Not fitted yet")
            return
        Kappa = eval('self._'+self.type+'(Xp, self.X, self.c1, self.c2, self.d)')
        return Kappa @ self.weights @ self.Y



"""
KRR=KernelRidgeRegression("gauss")
KRR.set_var(1,1,1,2)
KRR.fit(X,Y)
Y_predict_val=KRR.predict(X_v)
rmse_class=np.sqrt(np.mean(np.square(Y_predict_val-Y_v)))
print(rmse_class)
"""
