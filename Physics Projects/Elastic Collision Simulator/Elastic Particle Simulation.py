import matplotlib.pyplot as plt
import numpy as np
import random as rnd


class Particle:
    def __init__(self, name, group, mass, radius, charge):
        self.name = name
        self.group = group
        self.mass = mass
        self.radius = radius
        self.charge = charge


class ActiveParticle:
    def __init__(self, p_type, velocity):
        self.p_type = p_type
        self.position = []
        self.velocity = velocity

    def overlap_check(self, other, dt):
        if np.fabs(self.position[dt] - other.position[dt]) <= 10 and not self == other:
            return True
        else:
            return False


class Simulation:
    def __init__(self, timeDuration, timeStep, electron_count, electron_data, proton_count, proton_data, neutron_count,
                 neutron_data):
        self.time = np.arange(0, timeDuration, timeStep)
        self.dt = timeStep
        self.count_1 = electron_count
        self.count_2 = proton_count
        self.count_3 = neutron_count
        self.data_1 = electron_data
        self.data_2 = proton_data
        self.data_3 = neutron_data

    def Simulate(self, save):
        particles = []

        #Assign active particles
        for count in range(self.count_1 + self.count_2 + self.count_3):
            if count >= self.count_1 + self.count_2:
                particles.append(
                    ActiveParticle(self.data_3, rnd.randint(-int(sim_value_data[4]), int(sim_value_data[4]))))
            elif count >= self.count_1:
                particles.append(
                    ActiveParticle(self.data_2, rnd.randint(-int(sim_value_data[4]), int(sim_value_data[4]))))
            else:
                particles.append(
                    ActiveParticle(self.data_1, rnd.randint(-int(sim_value_data[4]), int(sim_value_data[4]))))

        #Increment particle values through  time
        for dt in range(int(float(sim_value_data[1]) / float(sim_value_data[2]))):
            for particle in particles:
                if dt == 0:
                    particle.position.append(rnd.randint(-int(sim_value_data[3]), int(sim_value_data[3])))

                    print(particle.position[0])
                    print(particle.velocity)
                else:
                    for o_particle in particles:
                        if particle.overlap_check(o_particle, dt - 1):
                            init_vel_part_1 = o_particle.velocity
                            init_vel_part_2 = particle.velocity

                            o_particle.velocity = (2 * particle.p_type.mass * init_vel_part_2 + init_vel_part_1 *
                                                (o_particle.p_type.mass - particle.p_type.mass)) / \
                                                (particle.p_type.mass + o_particle.p_type.mass)
                            particle.velocity = o_particle.velocity + init_vel_part_1 - init_vel_part_2

                            #o_particle.velocity = init_vel_part_1 * -1
                            #particle.velocity = init_vel_part_2 * -1

                    particle.position.append(particle.position[dt - 1] + particle.velocity * float(sim_value_data[2]))

        #Populate plot with data
        for particle in particles:
            if particle.p_type == self.data_1:
                Electron_plot = plt.plot(self.time, particle.position, color='b', label='Electron')
            elif particle.p_type == self.data_2:
                Proton_plot = plt.plot(self.time, particle.position, color='r', label='Proton')
            else:
                Neutron_plot = plt.plot(self.time, particle.position, color='y', label='Neutron')

        plt.title("Elementary Particle Elastic Collision Simulation")
        plt.ylabel("Displacement")
        plt.xlabel("Time")

        plt.legend(['Electrons: ' + str(particle_count_data[0]), 'Protons: ' + str(particle_count_data[1]), 'Neutrons: ' + str(particle_count_data[2])], loc='lower left')

        plt.grid(True)

        if save:
            plt.savefig(str(sim_value_data[0]) + " Simulation Result")
        else:
            plt.show()

    '''
    def calculateCollisions(self, p1, p2, p1_i_vel, p2_i_vel):
        p2.velocity = (2 * p1.mass * p1_i_vel + p2_i_vel * (p2.mass - p1.mass)) / (p2.mass + p1.mass)
        p1.velocity = p2_i_vel + p2.velocity - p1_i_vel
    '''


def fetchData():
    global sim_value_data, particle_count_data, particle_types

    with open(f'simulation_data/simulation_opt.txt', 'rt', encoding="utf8") as sim_opt:
        sim_opt_lines = sim_opt.readlines()

        sim_value_data = []

        for num in range(len(sim_opt_lines)):
            sim_data = sim_opt_lines[num].split(' ')

            if num != len(sim_opt_lines) - 1:
                subtract = 1
            else:
                subtract = 0

            sim_value = str(sim_data[len(sim_data) - 1])[:len(str(sim_data[len(sim_data) - 1])) - subtract]

            sim_value_data.append(sim_value)

    with open(f'./simulation_data/sim_particle sheets/{str(sim_value_data[0])}.txt', 'rt',
              encoding="utf8") as particles:
        particles_lines = particles.readlines()

        particle_count_data = []

        particle_types = []

        for num in range(len(particles_lines)):
            particle_data = particles_lines[num].split(':')

            particle_count_data.append(
                int(str(particle_data[len(particle_data) - 1])))

            particle = str(particle_data[0])

            with open(f'./simulation_data/sim_particle data/{particle}.txt', 'rt', encoding="utf8") as particles_sim:
                particle_data_lines = particles_sim.readlines()

                particle_data_values = []

                for count in range(len(particle_data_lines)):
                    particle_data = particle_data_lines[count].split(' ')

                    if count != len(particle_data_lines) - 1:
                        subtract = 1
                    else:
                        subtract = 0

                    particle_value = str(particle_data[len(particle_data) - 1])[
                                     :len(str(particle_data[len(particle_data) - 1])) - subtract]

                    particle_data_values.append(particle_value)
            
            particle_types.append(
                Particle(particle_data_values[0], particle_data_values[1], float(particle_data_values[2]),
                         float(particle_data_values[3]), int(particle_data_values[4])))


if __name__ == '__main__':
    fetchData()

    Sim = Simulation(float(sim_value_data[1]), float(sim_value_data[2]), particle_count_data[0], particle_types[0],
                     particle_count_data[1], particle_types[1], particle_count_data[2], particle_types[2])

    Sim.Simulate(True)
