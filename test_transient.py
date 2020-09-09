import src.rmf_tool as rmf
import numpy as np
from test_drift_derivatives import absolute_difference
import pickle

def sir_model():
    """
    this returns a density dependent population process of an SIR model
    """
    ddpp = rmf.DDPP()
    ddpp.add_transition([-1, 1, 0], lambda x: x[0]+2*x[0]*x[1])
    ddpp.add_transition([0, -1, +1], lambda x: x[1])
    ddpp.add_transition([1, 0, -1], lambda x: 3*x[2]**3)
    return ddpp

def to_be_tested(model, x0):
    """
    datas to be tested (from the model)
    """
    model.set_initial_state(x0)
    _,X = model.meanFieldExpansionTransient(order=0, time=3)
    _,X1,V1,_ = model.meanFieldExpansionTransient(order=1, time=3)
    _,X2,V2,A2,_ = model.meanFieldExpansionTransient(order=2, time=3)
    values = [X[-1], X1[-1], X2[-1], V1[-1], V2[-1]]
    return [array for mytuple in values for array in mytuple ]

def generate_data():
    """
    Generate a pickle file with the current version of the tool.
    """
    model = sir_model()
    data = dict([])
    for i in range(10):
        x0 = np.random.rand(3)
        x0 = x0/sum(x0)
        data[tuple(x0)] = to_be_tested(model, x0)
        print(x0)
    with open('output_tests/test_transient.pickle', 'wb') as f:
        # Pickle the 'data' dictionary using the highest protocol available.
        pickle.dump(data, f, pickle.HIGHEST_PROTOCOL)

def test_transient():
    """
    Test if derivatives are correct
    """
    model = sir_model()
    with open('output_tests/test_transient.pickle', 'rb') as f:
        data = pickle.load(f)
        for x0 in data:
            new_data = to_be_tested(model, np.array(x0))
            test_data = data[x0]
            assert absolute_difference(new_data, test_data) <= 1e-4

#generate_data()
#test_transient()