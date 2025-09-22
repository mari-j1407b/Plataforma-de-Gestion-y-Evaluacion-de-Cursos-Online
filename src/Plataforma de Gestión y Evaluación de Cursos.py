import os
class persona:
    def __init__(self, id_persona, nombre):
        self.id = id_persona
        self.nombre = nombre
    
    def __str__(self):
        return f"Persona(ID: {self.id}, Nombre: {self.nombre})"
        
class estudiantess(persona):
    def __init__(self, id_estudiante, nombre):
        super().__init__(id_estudiante, nombre)
        self.cursos_inscritos = []
        self.calificaciones = {}

    def inscribir_curso(self, curso):
        if curso not in self.cursos_inscritos:
            self.cursos_inscritos.append(curso)
            curso.estudiantes_inscritos.append(self)
            return True
        return False
    
    def __str__(self):
        return f"Estudiante(ID: {self.id}, Nombre: {self.nombre}, Cursos: {len(self.cursos_inscritos)})"
            
class profesorr(persona):
    def __init__(self, id_profesor, nombre):
        super().__init__(id_profesor, nombre)
        self.cursos_impartidos = []
    
    def crear_curso(self, sistema, nombre_del_curso, codigo_del_curso):
        for curso in sistema.cursos:
            if curso.codigo == codigo_del_curso:
                print(f"Ya existe un curso con el código {codigo_del_curso}")
                return None
        
        curso = Curso(nombre_del_curso, codigo_del_curso, self)
        sistema.registrar_curso(curso)
        self.cursos_impartidos.append(curso)
        return curso
    
    def __str__(self):
        return f"Profesor(ID: {self.id}, Nombre: {self.nombre}, Cursos: {len(self.cursos_impartidos)})"