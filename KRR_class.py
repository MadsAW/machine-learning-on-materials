import numpy as np
import numexpr as ne
# Heat of formation vs heat of formation predicted point plot
# fit x to sin(x)
# or use cos
class KernelRidgeRegression:
    """KernelRidgeRegression
    This class creates a kernel ridge regression model that can be used for
    fitting. Upon initializaiton the following can be specified:

    - type, specifies the type can be one of ["linear","laplace","gauss","poly"]
        specifying the kernel space. Defaults to "linear".
    - lambd, the regularization constant
    - sigma, sets sigma for laplacian or gauss, note overwrites c1.
    - c1, first koefficent for linear and poly overwrites sigma.
    - c2, second koefficent
    - d, third koeeficent only used in poly

    Note all values default to 1


    ADD DIMENSION CHECK
    """
    def __init__(self, **kwargs):
        self.lambd = kwargs.get("lambd",1)
        self.c1=1
        if "c1" in kwargs:
            self.c1 = kwargs.get("c1",1)
        if "sigma" in kwargs:
            self.c1 = kwargs.get("sigma",1)
        self.c2 = kwargs.get("c2",1)
        self.d = kwargs.get("d",1)
        type = kwargs.get("type","linear")
        if type in ["linear","laplace","gauss","poly"]:
            self.type=type
        else:
            self.type="linear"
            print("Illegal type assignment, note allowed types are linear, \
                laplace, gauss, poly, defaulting to linear model")
        self.weigths = []
        self.fitted = False
        self.rmse = None

    def _subt(self, A, B):
        A_3D = A[:, np.newaxis]
        return ne.evaluate('A_3D - B')
        #return A_3D - B
    #Linear
    def _linear(self, A, B, c, *args):
        return np.tensordot(A,B,axes=([1],[1]))+c

    #Polynomial
    def _poly(self, A, B, c1, c2, d, *args):
        return np.power(c1*np.tensordot(A,B,axes=([1],[1]))+c2,d)

    #Gaussian
    def _gauss(self, A, B, sigma, *args):
        K=np.zeros((len(A),len(B)))
        for i in range(0, len(A)):
            for j in range(0, len(B)):
                K[i,j]=np.exp(-np.square(np.linalg.norm(A[i]-B[j]))/(2*(sigma**2)))
        return K
        #A=A[:,np.newaxis]
        #return np.exp(   -np.square(np.linalg.norm(A-B, axis=2)) / (2*(sigma**2))    )
        #return np.exp(   -np.square(np.linalg.norm(self._subt(A,B), axis=2)) / (2*(sigma**2))    )

    #Laplacian
    def _laplace(self, A, B, sigma, *args):
        K=np.zeros((len(A),len(B)))
        for i in range(0, len(A)):
            for j in range(0, len(B)):
                K[i,j]=np.exp(-np.linalg.norm(A[i]-B[j])/(sigma))
        return K
        #return np.exp(   -(np.linalg.norm(self._subt(A,B), axis=2)) /  sigma    )

    def _clear(self):
        self.weigths = []
        self.fitted = False
        self.rmse = None

    def _check_dim(self, A, B):
        if(A.shape[0]!=B.shape[0]):
            raise ValueError("Dimension do not match")

    def set_var(self,**kwargs):
        self.lambd = kwargs.get("lambd",1)
        if "c1" in kwargs:
            self.c1 = kwargs.get("c1",1)
        if "sigma" in kwargs:
            self.c1 = kwargs.get("sigma",1)
        self.c2 = kwargs.get("c2",1)
        self.d = kwargs.get("d",1)
        self._clear()
    def set_type(self, type):
        type = kwargs.get("type","linear")
        if type in ["linear","laplace","gauss","poly"]:
            self.type=type
        else:
            self.type="linear"
            print("Illegal type assignment, note allowed types are linear, \
                laplace, gauss, poly, defaulting to linear model")
        self._clear()
    def fit(self, X, Y):
        if (self.fitted == False):
            self._check_dim(X,Y)
            self.X = X
            self.Y = Y
            K = eval('self._'+self.type+'(self.X, self.X, self.c1, self.c2, self.d)')
            I = np.identity(len(X))
            self.weights = np.linalg.inv(np.matrix(K+self.lambd*I))
            self.fitted = True
        else:
            print("already fitted")
    def predict(self, Xp, Y=[]):
        if (self.fitted == False):
            print("Not fitted yet")
            return
        Kappa = eval('self._'+self.type+'(Xp, self.X, self.c1, self.c2, self.d)')
        Y_predicted=Kappa @ self.weights @ self.Y
        if (Y!=[]):
            self._check_dim(Y_predicted.T,Y)
            self.rmse=np.sqrt(np.mean(np.square(Y_predicted-Y)))
        return Y_predicted



"""
KRR=KernelRidgeRegression(type = "gauss")
KRR.fit(X,Y)
Y_predict_val=KRR.predict(X_v)
rmse_class=np.sqrt(np.mean(np.square(Y_predict_val-Y_v)))
print(rmse_class)
"""
