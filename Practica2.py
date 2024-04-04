"""Cola de espera en una clínica del IMSS."""
import random

class Persona:
    def __init__(self, tiempo_llegada, es_emergencia):
        self.tiempo_llegada = tiempo_llegada
        self.es_emergencia = es_emergencia
        self.tiempo_atencion = 30 if not es_emergencia else 0  # 30 minutos para rutinarios, 0 minutos para emergencias

class Cola:
    def __init__(self, reloj):
        self.cola = []
        self.reloj = reloj

    def agregar_persona(self, persona):
        self.cola.append(persona)

    def remover_persona(self):
        return self.cola.pop(0)

    def obtener_tiempo_espera_actual(self):
        if not self.cola:
            return 0
        else:
            return (self.reloj + self.cola[0].tiempo_atencion) - self.cola[0].tiempo_llegada

class Simulacion:
    def __init__(self):
        self.reloj = 0
        self.cola = Cola(self.reloj)
        self.tiempo_espera_total = 0
        self.tiempo_atencion_total = 0

    def simular(self, num_personas):
        for i in range(num_personas):
            # Generar tiempo de llegada y tipo de paciente
            tiempo_llegada = random.uniform(0.5, 50)
            es_emergencia = random.random() < 0.20  # 20% de probabilidad

            # Actualizar reloj
            self.reloj += tiempo_llegada

            # Crear nueva persona
            nueva_persona = Persona(self.reloj, es_emergencia)

            # Agregar persona a la cola
            self.cola.agregar_persona(nueva_persona)

            # Verificar si la persona al frente de la cola puede ser atendida
            if self.cola.obtener_tiempo_espera_actual() + nueva_persona.tiempo_atencion <= 30:
                persona_atendida = self.cola.remover_persona()
                self.tiempo_espera_total += self.cola.obtener_tiempo_espera_actual()
                self.tiempo_atencion_total += persona_atendida.tiempo_atencion

        promedio_tiempo_espera = self.tiempo_espera_total / num_personas
        promedio_tiempo_atencion = self.tiempo_atencion_total / num_personas

        return promedio_tiempo_espera, promedio_tiempo_atencion

# Realizar 20 simulaciones
for i in range(20):
    promedio_tiempo_espera, promedio_tiempo_atencion = Simulacion().simular(50000)
    print(f"Simulación {i+1}: tiempo de espera = {promedio_tiempo_espera:.2f}, tiempo de atención = {promedio_tiempo_atencion:.2f}")







"""Cola de espera en una clínica del IMSS."""
import random

class Persona:
    def __init__(self, tiempo_llegada, es_emergencia):
        self.tiempo_llegada = tiempo_llegada
        self.es_emergencia = es_emergencia
        self.tiempo_atencion = 20 if not es_emergencia else 0  # 20 minutos para rutinarios, 0 minutos para emergencias

class Cola:
    def __init__(self, reloj):
        self.cola = []
        self.reloj = reloj

    def agregar_persona(self, persona):
        self.cola.append(persona)

    def remover_persona(self):
        return self.cola.pop(0)

    def obtener_tiempo_espera_actual(self):
        if not self.cola:
            return 0
        else:
            return (self.reloj + self.cola[0].tiempo_atencion) - self.cola[0].tiempo_llegada

class Simulacion:
    def __init__(self):
        self.reloj = 0
        self.cola = Cola(self.reloj)
        self.tiempo_espera_total = 0
        self.tiempo_atencion_total = 0

    def simular(self, num_personas):
        for i in range(num_personas):
            # Generar tiempo de llegada y tipo de paciente
            tiempo_llegada = random.uniform(0.5, 50)
            es_emergencia = random.random() < 0.20  # 20% de probabilidad

            # Actualizar reloj
            self.reloj += tiempo_llegada

            # Crear nueva persona
            nueva_persona = Persona(self.reloj, es_emergencia)

            # Agregar persona a la cola
            self.cola.agregar_persona(nueva_persona)

            # Verificar si la persona al frente de la cola puede ser atendida
            if self.cola.obtener_tiempo_espera_actual() <= 20 - nueva_persona.tiempo_atencion:
                persona_atendida = self.cola.remover_persona()
                self.tiempo_espera_total += self.cola.obtener_tiempo_espera_actual()
                self.tiempo_atencion_total += persona_atendida.tiempo_atencion

        promedio_tiempo_espera = self.tiempo_espera_total / num_personas
        promedio_tiempo_atencion = self.tiempo_atencion_total / num_personas

        return promedio_tiempo_espera, promedio_tiempo_atencion

# Realizar 20 simulaciones
for i in range(20):
    promedio_tiempo_espera, promedio_tiempo_atencion = Simulacion().simular(50000)
    print(f"Simulación {i+1}: tiempo de espera = {promedio_tiempo_espera:.2f}, tiempo de atención = {promedio_tiempo_atencion:.2f}")







"""Cola de espera en una clínica del IMSS."""
import random

class Persona:
    def __init__(self, llegada, tipo):
        self.llegada = llegada
        self.tipo = tipo

class Cola:
    def __init__(self):
        self.pacientes = []

    def add_paciente(self, paciente):
        self.pacientes.append(paciente)

    def atender_paciente(self):
        if self.pacientes:
            return self.pacientes.pop(0)

class Simulacion:
    def __init__(self):
        self.cola = Cola()
        self.tiempo_simulacion = 0
        self.tiempo_espera = []

    def simular(self, num_pacientes, atencion_min, atencion_max):
        self.atencion_min = atencion_min
        self.atencion_max = atencion_max

        for _ in range(num_pacientes):
            llegada = random.uniform(atencion_min, atencion_max)
            tipo = random.random() < 0.2  # 20% ser de urgencia
            self.cola.add_paciente(Persona(llegada, tipo))

        while self.cola.pacientes:
            if self.tiempo_simulacion >= self.cola.pacientes[0].llegada:
                paciente = self.cola.atender_paciente()
                self.tiempo_espera.append(self.tiempo_simulacion - paciente.llegada)

                # 30 min de consulta
                self.tiempo_simulacion += 30
            else:
                self.tiempo_simulacion = self.cola.pacientes[0].llegada

        return self.tiempo_espera

def run_simulation(num_pacientes, num_runs, atencion_min, atencion_max):
    total_tiempo_espera = []

    for _ in range(num_runs):
        simulacion = Simulacion()
        tiempos_espera = simulacion.simular(num_pacientes, atencion_min, atencion_max)
        total_tiempo_espera.append(sum(tiempos_espera) / len(tiempos_espera))

    avg_tiempo_espera = sum(total_tiempo_espera) / len(total_tiempo_espera)
    avg_tiempo_sistema = avg_tiempo_espera + atencion_max

    return avg_tiempo_espera, avg_tiempo_sistema

# Parametros
num_pacientes = 50_000
num_runs = 20
atencion_min = 0.5
atencion_max = 50

# Ejecutar simulacion
avg_tiempo_espera, avg_tiempo_sistema = run_simulation(num_pacientes, num_runs, atencion_min, atencion_max)

print(f"Tiempo promedio de espera: {avg_tiempo_espera:.2f} minutes")
print(f"Tiempo promedio en el sistema: {avg_tiempo_sistema:.2f} minutes")







"""Cola de espera en una clínica del IMSS."""
import random

class Persona:
    def __init__(self, llegada, tipo):
        self.llegada = llegada
        self.tipo = tipo

class Cola:
    def __init__(self):
        self.pacientes = []

    def add_paciente(self, paciente):
        self.pacientes.append(paciente)

    def atender_paciente(self):
        if self.pacientes:
            return self.pacientes.pop(0)

class Simulacion:
    def __init__(self):
        self.cola = Cola()
        self.tiempo_simulacion = 0
        self.tiempo_espera = []

    def simular(self, num_pacientes, atencion_min, atencion_max):
        self.atencion_min = atencion_min
        self.atencion_max = atencion_max

        for _ in range(num_pacientes):
            llegada = random.uniform(atencion_min, atencion_max)
            tipo = random.random() < 0.2  # 20% ser de urgencia
            self.cola.add_paciente(Persona(llegada, tipo))

        while self.cola.pacientes:
            if self.tiempo_simulacion >= self.cola.pacientes[0].llegada:
                paciente = self.cola.atender_paciente()
                self.tiempo_espera.append(self.tiempo_simulacion - paciente.llegada)

                # 30 min de consulta
                self.tiempo_simulacion += 20
            else:
                self.tiempo_simulacion = self.cola.pacientes[0].llegada

        return self.tiempo_espera

def run_simulation(num_pacientes, num_runs, atencion_min, atencion_max):
    total_tiempo_espera = []

    for _ in range(num_runs):
        simulacion = Simulacion()
        tiempos_espera = simulacion.simular(num_pacientes, atencion_min, atencion_max)
        total_tiempo_espera.append(sum(tiempos_espera) / len(tiempos_espera))

    avg_tiempo_espera = sum(total_tiempo_espera) / len(total_tiempo_espera)
    avg_tiempo_sistema = avg_tiempo_espera + atencion_max

    return avg_tiempo_espera, avg_tiempo_sistema

# Parametros
num_pacientes = 50_000
num_runs = 20
atencion_min = 0.5
atencion_max = 50

# Ejecutar simulacion
avg_tiempo_espera, avg_tiempo_sistema = run_simulation(num_pacientes, num_runs, atencion_min, atencion_max)

print(f"Tiempo promedio de espera: {avg_tiempo_espera:.2f} minutes")
print(f"Tiempo promedio en el sistema: {avg_tiempo_sistema:.2f} minutes")
