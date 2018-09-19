# Create your first MLP in Keras
from keras.models import Sequential
from keras.layers import Dense
import numpy
import ase.db
import fingerprint
#Import as db object
db = ase.db.connect('binaryalloys.db')
"""

cursor=db.cursor

cursor.execute("SQL COMMAND")  # execute a simple SQL select query
jobs = cursor.fetchall()  # get all the results from the above query

"""
#variables in [Å]
rmax=10.0 #max distance to look at
dr=0.2#steps
rs=np.arrange(0, rmax-dr, dr/5)#list of steps

atoms=[]
for row in db.select():
    atoms.append(db.get_atoms(row['id'])

for atom in atoms:
    fingerprint.prdf(atom, rs, dr, rmax)
"""
# fix random seed for reproducibility
numpy.random.seed(7)
# load pima indians dataset
dataset = numpy.loadtxt("pima-indians-diabetes.csv", delimiter=",")
# split into input (X) and output (Y) variables
X = dataset[:,0:8]
Y = dataset[:,8]
# create model
model = Sequential()
model.add(Dense(12, input_dim=8, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(12, activation='relu'))
model.add(Dense(8, activation='relu'))
model.add(Dense(1, activation='sigmoid'))
# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# Fit the model
model.fit(X, Y, epochs=150, batch_size=10)
# evaluate the model
scores = model.evaluate(X, Y)
print("\n%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))
"""
