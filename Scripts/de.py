#import rhinoscriptsyntax as rs
import random
import copy

POPULATION_SIZE = 100    
DIMENSION = 4           
NUMBER_IT = 10000       
SCALING_FACTOR = 0.5
CROSSOVER_PROB = 0.7
first = True
population = []
class Vector:
    def __init__(self, orientation, window_w, window_e, transmitance, fxv=None):
        self.orientation = orientation
        self.window_w = window_w
        self.window_e = window_e
        self.transmitance = transmitance
        self.fxv = fxv

    def __str__(self):
        return f"Orientation: {self.orientation}, Window W: {self.window_w}, Window E: {self.window_e}, Transmitance: {self.transmitance}, fx: {self.fxv}"
    

def sub_vectors(vector1, vector2):
    orientation_diff = vector1.orientation - vector2.orientation
    window_w_diff = vector1.window_w - vector2.window_w
    window_e_diff = vector1.window_e - vector2.window_e
    transmitance_diff = vector1.transmitance - vector2.transmitance
    
    difference_vector = Vector(orientation_diff, window_w_diff, window_e_diff, transmitance_diff)
    
    return difference_vector

def sum_vectors(vector1, vector2):
    orientation_result = vector1.orientation + vector2.orientation
    window_w_result = vector1.window_w + vector2.window_w
    window_e_result = vector1.window_e + vector2.window_e
    transmitance_result = vector1.transmitance + vector2.transmitance
    
    result_vector = Vector(orientation_result, window_w_result, window_e_result, transmitance_result)
    
    return result_vector

def clip_value(value, min_value, max_value):
    # Verifica se o valor está abaixo do mínimo e ajusta para o mínimo
    if value < min_value:
        return min_value
    # Verifica se o valor está acima do máximo e ajusta para o máximo
    if value > max_value:
        return max_value
    # Caso contrário, retorna o valor original
    return value

def is_vector_in_range(vector):
    orientation_min, orientation_max = -180.0, 180.0
    window_w_min, window_w_max = 0.1, 5.9
    window_e_min, window_e_max = 0.1, 5.9
    transmitance_min, transmitance_max = 0.2, 0.8

    # Ajusta os valores das variáveis do Vector para que estejam dentro dos limites permitidos
    orientation = clip_value(vector.orientation, orientation_min, orientation_max)
    window_w = clip_value(vector.window_w, window_w_min, window_w_max)
    window_e = clip_value(vector.window_e, window_e_min, window_e_max)
    transmitance = clip_value(vector.transmitance, transmitance_min, transmitance_max)

    return Vector(orientation, window_w, window_e, transmitance, fxv=vector.fxv)

def mult_vector_by_constant(vector, constant):
    orientation_result = vector.orientation * constant
    window_w_result = vector.window_w * constant
    window_e_result = vector.window_e * constant
    transmitance_result = vector.transmitance * constant
    
    result_vector = Vector(orientation_result, window_w_result, window_e_result, transmitance_result)
    
    return result_vector

def inicializePopulation():
    for i in range(POPULATION_SIZE):
        orientation = random.uniform(-180.0, 180.0)
        window_w = random.uniform(0.1, 5.9)
        window_e = random.uniform(0.1, 5.9)
        transmitance = random.uniform(0.2, 0.8)
        vetor = Vector(orientation, window_w, window_e, transmitance)
        #Calcular fxv com o simulador
        vetor.fxv = calcFx(vetor)
        population.append(vetor)

    print("Inicio")
    for i in population:
        print(i)


def mutation():
    population_copia = copy.deepcopy(population)

    target_vector = random.choice(population_copia)
    population_copia.remove(target_vector)

    sol_1 = random.choice(population_copia)
    population_copia.remove(sol_1)

    sol_2 = random.choice(population_copia)
    population_copia.remove(sol_2)

    #Subtrai os vetores
    sub_sol = sub_vectors(sol_1, sol_2)
    #multiplica o sub_sol por Scaling_Factor
    sub_sol = mult_vector_by_constant(sub_sol, SCALING_FACTOR)


    trial_vector = sum_vectors(target_vector, sub_sol)
    trial_vector = is_vector_in_range(trial_vector)

    parent_vector = random.choice(population_copia)
    parent_index = population_copia.index(parent_vector)

    return trial_vector, parent_index

def crossover(trial_vector, parent_vector):
    i_set = []
    i_set.append(random.randint(0,DIMENSION-1))

    for j in range(DIMENSION):
        if((j!=i_set[0]) and (random.uniform(0,1)<CROSSOVER_PROB)):
            i_set.append(j)

    trial_list = [trial_vector.orientation, trial_vector.window_w, trial_vector.window_e, trial_vector.transmitance, trial_vector.fxv]
    parent_list = [parent_vector.orientation, parent_vector.window_w, parent_vector.window_e,parent_vector.transmitance, parent_vector.fxv]
    offspring = [0,0,0,0,None]
    for i in range(DIMENSION):
        if i in i_set:
            offspring[i] = trial_list[i]
        else:
            offspring[i] = parent_list[i]

    x1 = Vector(offspring[0], offspring[1],offspring[2],offspring[3],None)
    return x1

def calcFx(vector):
    return vector.orientation + vector.window_w + vector.window_e + vector.transmitance
        

inicializePopulation()

for i in range(NUMBER_IT):
    result = mutation()
    trial_v, parent_index = result
    parent_v = population[parent_index]
    x1 = crossover(trial_v, parent_v)
    # Calcular fx1 pelo simulador Grasshopper
    x1.fxv = calcFx(x1)

    if(x1.fxv<parent_v.fxv):
        population.remove(parent_v)
        population.append(x1)

print("Fim")
for i in population:
    print(i)
