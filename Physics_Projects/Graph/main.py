import matplotlib.pyplot as plt
import numpy as np

springCoeficients = [9, 9, 81]
frictionCoeficients = [18, 6, 1]

springCoeficient = 2
frictionCoeficient = 1
objectMass = 1

t = 0
x = 0

x_0 = 0
v_0 = 10


def solver(s_coef, f_coef, obj_m):
    global t, x
    lamda = f_coef / (2 * obj_m)
    omega = np.sqrt(s_coef / obj_m)

    delta = (lamda - omega) * (lamda + omega)
    sqrt_delta = np.sqrt(np.abs(delta))

    t = np.arange(0, 10, 0.01)
    x = np.exp(-lamda * t)

    if delta > 0:
        A = (v_0 + x_0 * (lamda + sqrt_delta))
        B = x_0 - A

        x *= (A * np.exp(sqrt_delta * t) + B * np.exp(-sqrt_delta * t))
        print("Overdamped oscilator")
    elif delta == 0:
        A = x_0
        B = v_0 + lamda * A

        x *= (A + B * t)
        print("Critically damped oscilator")
    elif delta < 0:
        A = x_0
        B = (v_0 / (lamda * sqrt_delta))

        x *= (A * np.cos(sqrt_delta * t) + B * np.sin(sqrt_delta * t))
        print("Underdamped oscilator")


def plot(var_1, var_1_label, var_2, var_2_label, save):
    fig, axs = plt.subplots(3)
    axs[iter].plot(t, x)
    # plt.plot(var_1, var_2, color="Blue")
    # plt.plot(var_1, var_2, color="Blue")
    # plt.plot(var_1, var_2, color="Blue")
    plt.xlabel(var_1_label)
    plt.ylabel(var_2_label)
    plt.title("Damped Harmonic Oscilator")
    plt.legend(
        ['Spring Coeficient( k ): ' + str(springCoeficient), 'Friction Coeficient( a ): ' + str(frictionCoeficient),
         'Object mass( m ): ' + str(objectMass)], loc='lower left')

    if save:
        plt.savefig(str("Simulation Result"))
    else:
        plt.show()


if __name__ == "__main__":
    for iter in range(0, 3):
        solver(springCoeficient, frictionCoeficient, objectMass)

    plot(t, "Time", x, "Displacement", False)

    print("Programmed by Kiril Ivanov.")
