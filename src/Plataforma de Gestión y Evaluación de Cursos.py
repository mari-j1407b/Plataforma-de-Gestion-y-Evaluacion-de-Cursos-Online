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
    
class Curso:
    def __init__(self, nombre, codigo, profesor):
        self.nombre = nombre 
        self.codigo = codigo
        self.profesor = profesor
        self.estudiantes_inscritos = []
        self.evaluaciones = []
    
    def agregar_evaluacion(self, evaluacion):
        for eval_existente in self.evaluaciones:
            if eval_existente.nombre.lower() == evaluacion.nombre.lower():
                print(f"Ya existe una evaluación con el nombre '{evaluacion.nombre}' en este curso")
                return False
        self.evaluaciones.append(evaluacion)
        return True
    
    def listar_evaluaciones(self):
        if not self.evaluaciones:
            return "No hay evaluaciones registradas"
        return "\n".join([f"{i+1}. {eval.nombre} (ID: {eval.id})" for i, eval in enumerate(self.evaluaciones)])
    
    def __str__(self):
        return f"Curso(Código: {self.codigo}, Nombre: {self.nombre}, Profesor: {self.profesor.nombre})"
        
class evaluacionn:
    def __init__(self, id_evaluacion, nombre, fecha, nota_maxima, tipo, curso_codigo):
        self.id = id_evaluacion
        self.nombre = nombre
        self.fecha = fecha
        self.nota_maxima = nota_maxima
        self.tipo = tipo
        self.curso_codigo = curso_codigo
        self.calificaciones = {}
        
    def registrar_calificacion(self, estudiante, calificacion):
        if calificacion < 0 or calificacion > self.nota_maxima:
            print(f"La calificación debe estar entre 0 y {self.nota_maxima}")
            return False
        
        self.calificaciones[estudiante.id] = calificacion
        
        if estudiante.id not in estudiante.calificaciones:
            estudiante.calificaciones[estudiante.id] = {}
        
        estudiante.calificaciones[estudiante.id][self.id] = calificacion
        return True
    
    def __str__(self):
        return f"Evaluación(ID: {self.id}, Nombre: {self.nombre}, Tipo: {self.tipo}, Curso: {self.curso_codigo})"
    
class sistema_de_gestion_de_cursos:
    def __init__(self):
        self.estudiantes = []
        self.profesores = []
        self.cursos = []
        self.evaluaciones = []
        
    def registrar_estudiante(self, id_est, nombre):
        for estudiante in self.estudiantes:
            if estudiante.id == id_est:
                print(f"Ya existe un estudiante con ID {id_est}")
                return estudiante
        nuevo_estudiante = estudiantess(id_est, nombre)
        self.estudiantes.append(nuevo_estudiante)
        return nuevo_estudiante
    
    def registrar_profesor(self, id_inst, nombre):
        for instructor in self.profesores:
            if instructor.id == id_inst:
                print(f"Ya existe un profesor con ID {id_inst}")
                return instructor
        nuevo_instructor = profesorr(id_inst, nombre)
        self.profesores.append(nuevo_instructor)
        return nuevo_instructor
    
    def registrar_curso(self, curso):
        for c in self.cursos:
            if c.codigo == curso.codigo:
                print(f"Ya existe un curso con código {curso.codigo}")
                return c
        self.cursos.append(curso)
        return curso
    
    def crear_evaluacion(self, curso_id, nombre, tipo, fecha_limite, puntaje_maximo, evaluacion_id):
        curso = next((c for c in self.cursos if c.codigo == curso_id), None)
        if not curso:
            print(f"No existe el curso con código {curso_id}")
            return None
        
        for eval_existente in self.evaluaciones:
            if eval_existente.id == evaluacion_id:
                print(f"Ya existe una evaluación con ID {evaluacion_id}")
                return None
        
        nueva_evaluacion = evaluacionn(evaluacion_id, nombre, fecha_limite, puntaje_maximo, tipo, curso_id)
        
        if curso.agregar_evaluacion(nueva_evaluacion):
            self.evaluaciones.append(nueva_evaluacion)
            return nueva_evaluacion
        return None

    def inscribir_estudiante_en_curso(self, estudiante_id, curso_id):
        estudiante = next((e for e in self.estudiantes if e.id == estudiante_id), None)
        curso = next((c for c in self.cursos if c.codigo == curso_id), None)
        
        if not estudiante:
            print(f"No existe el estudiante con ID {estudiante_id}")
            return False
        if not curso:
            print(f"No existe el curso con código {curso_id}")
            return False
        
        return estudiante.inscribir_curso(curso)
    
    def registrar_calificacion(self, evaluacion_id, estudiante_id, calificacion):
        evaluacion = next((e for e in self.evaluaciones if e.id == evaluacion_id), None)
        estudiante = next((e for e in self.estudiantes if e.id == estudiante_id), None)
        
        if not evaluacion:
            print(f"No existe la evaluación con ID {evaluacion_id}")
            return False
        if not estudiante:
            print(f"No existe el estudiante con ID {estudiante_id}")
            return False
        
        curso_evaluacion = next((c for c in self.cursos if c.codigo == evaluacion.curso_codigo), None)
        if curso_evaluacion and estudiante not in curso_evaluacion.estudiantes_inscritos:
            print(f"El estudiante no está inscrito en el curso {evaluacion.curso_codigo}")
            return False
        
        return evaluacion.registrar_calificacion(estudiante, calificacion)
    
    def obtener_promedio_estudiante(self, estudiante_id, curso_id=None):
        estudiante = next((e for e in self.estudiantes if e.id == estudiante_id), None)
        if not estudiante:
            print(f"No existe el estudiante con ID {estudiante_id}")
            return None
        
        if curso_id:
            curso = next((c for c in self.cursos if c.codigo == curso_id), None)
            if not curso:
                print(f"No existe el curso con código {curso_id}")
                return None
            
            if estudiante not in curso.estudiantes_inscritos:
                print(f"El estudiante no está inscrito en el curso {curso_id}")
                return None
            
            if estudiante_id in estudiante.calificaciones:
                calificaciones_curso = []
                for eval_id, calif in estudiante.calificaciones[estudiante_id].items():
                    eval_obj = next((e for e in self.evaluaciones if e.id == eval_id), None)
                    if eval_obj and eval_obj.curso_codigo == curso_id:
                        calificaciones_curso.append(calif)
                if calificaciones_curso:
                    return sum(calificaciones_curso) / len(calificaciones_curso)
            return None
        else:
            todas_calificaciones = []
            if estudiante_id in estudiante.calificaciones:
                for calif in estudiante.calificaciones[estudiante_id].values():
                    todas_calificaciones.append(calif)
            if todas_calificaciones:
                return sum(todas_calificaciones) / len(todas_calificaciones)
            return None
    
    def listar_cursos(self):
        if not self.cursos:
            return "No hay cursos registrados"
        return "\n".join([f"{i+1}. {curso.nombre} (Código: {curso.codigo})" for i, curso in enumerate(self.cursos)])
    
    def listar_estudiantes(self):
        if not self.estudiantes:
            return "No hay estudiantes registrados"
        return "\n".join([f"{i+1}. {est.nombre} (ID: {est.id})" for i, est in enumerate(self.estudiantes)])
    
    def listar_profesores(self):
        if not self.profesores:
            return "No hay profesores registrados"
        return "\n".join([f"{i+1}. {prof.nombre} (ID: {prof.id})" for i, prof in enumerate(self.profesores)])
    
    def listar_evaluaciones_curso(self, curso_id):
        curso = next((c for c in self.cursos if c.codigo == curso_id), None)
        if not curso:
            return f"No existe el curso con código {curso_id}"
        return curso.listar_evaluaciones()
    
    def listar_estudiantes_curso(self, curso_id):
        curso = next((c for c in self.cursos if c.codigo == curso_id), None)
        if not curso:
            return f"No existe el curso con código {curso_id}"
        if not curso.estudiantes_inscritos:
            return "No hay estudiantes inscritos en este curso"
        return "\n".join([f"{i+1}. {est.nombre} (ID: {est.id})" for i, est in enumerate(curso.estudiantes_inscritos)])
    
    def estudiantes_promedio_bajo(self, curso_id=None, limite=60):
        resultados = [] 
        for estudiante in self.estudiantes:
            promedio = self.obtener_promedio_estudiante(estudiante.id, curso_id)
            if promedio is not None and promedio < limite:
                resultados.append((estudiante, promedio))
        return resultados
    
    def estudiantes_promedio_alto(self, curso_id=None, limite=90):
        resultados = [] 
        for estudiante in self.estudiantes:
            promedio = self.obtener_promedio_estudiante(estudiante.id, curso_id)
            if promedio is not None and promedio > limite:
                resultados.append((estudiante, promedio))
        return resultados

def menu():
    sistema = sistema_de_gestion_de_cursos()
    
    while True:
        os.system('cls')
        print("\n" + "="*50)
        print("Sistema de Gestión de Cursos")
        print("="*50)
        print("1. Registrar Estudiante")
        print("2. Registrar Profesor")
        print("3. Crear Curso")
        print("4. Inscribir Estudiante en Curso")
        print("5. Crear Evaluación")
        print("6. Registrar Calificación")
        print("7. Obtener Promedio Estudiante")
        print("8. Listar Estudiantes con Promedio Bajo")
        print("9. Listar Estudiantes con Promedio Alto")
        print("10. Listar Cursos")
        print("11. Listar Estudiantes")
        print("12. Listar Evaluaciones de un Curso")
        print("13. Listar Profesores")
        print("14. Listar Estudiantes de un Curso")
        print("0. Salir")
        
        opcion = input("\nSeleccione una opción: ")

        if opcion == "1":
            os.system('cls')
            id_est = input("Ingrese el ID del estudiante: ")
            nombre = input("Ingrese el nombre del estudiante: ")
            estudiante = sistema.registrar_estudiante(id_est, nombre)
            if estudiante:
                print(f"Estudiante registrado: {estudiante}")
            
        elif opcion == "2":
            os.system('cls')
            id_inst = input("Ingrese el ID del profesor: ")
            nombre = input("Ingrese el nombre del profesor: ")
            profesor = sistema.registrar_profesor(id_inst, nombre)
            if profesor:
                print(f"Profesor registrado: {profesor}")
            
        elif opcion == "3":
            os.system('cls')
            codigo_curso = input("Ingrese el código del curso: ")
            nombre_curso = input("Ingrese el nombre del curso: ")
            profesor_id = input("Ingrese el ID del profesor: ")
            profesor = next((p for p in sistema.profesores if p.id == profesor_id), None)
            if not profesor:
                print("Profesor no encontrado.")
                continue
            curso = profesor.crear_curso(sistema, nombre_curso, codigo_curso)
            if curso:
                print(f"Curso creado: {curso}")
            
        elif opcion == "4":
            os.system('cls')
            print("\nEstudiantes disponibles:")
            print(sistema.listar_estudiantes())
            print("\nCursos disponibles:")
            print(sistema.listar_cursos())
            
            estudiante_id = input("\nIngrese el ID del estudiante: ")
            curso_id = input("Ingrese el código del curso: ")
            if sistema.inscribir_estudiante_en_curso(estudiante_id, curso_id):
                print("Estudiante inscrito en el curso.")
            
        elif opcion == "5":
            os.system('cls')
            print("\nCursos disponibles:")
            print(sistema.listar_cursos())
            
            curso_id = input("\nIngrese el código del curso: ")
            nombre = input("Ingrese el nombre de la evaluación: ")
            tipo = input("Ingrese el tipo de evaluación (examen/tarea): ")
            fecha_limite = input("Ingrese la fecha límite (YYYY-MM-DD): ")
            puntaje_maximo = int(input("Ingrese el puntaje máximo: "))
            evaluacion_id = input("Ingrese el ID de la evaluación: ")
            
            evaluacion = sistema.crear_evaluacion(curso_id, nombre, tipo, fecha_limite, puntaje_maximo, evaluacion_id)
            if evaluacion:
                print(f"Evaluación creada: {evaluacion}")
                
        elif opcion == "6":
            os.system('cls')
            print("\nCursos disponibles:")
            print(sistema.listar_cursos())
            
            curso_id = input("\nIngrese el código del curso: ")
            print(sistema.listar_evaluaciones_curso(curso_id))
            
            evaluacion_id = input("\nIngrese el ID de la evaluación: ")
            print("\nEstudiantes inscritos en el curso:")
            curso = next((c for c in sistema.cursos if c.codigo == curso_id), None)
            if curso:
                for i, est in enumerate(curso.estudiantes_inscritos):
                    print(f"{i+1}. {est.nombre} (ID: {est.id})")
            
            estudiante_id = input("\nIngrese el ID del estudiante: ")
            calificacion = float(input("Ingrese la calificación: "))
            
            if sistema.registrar_calificacion(evaluacion_id, estudiante_id, calificacion):
                print("Calificación registrada.")
                
        elif opcion == "7":
            os.system('cls')
            print("\nEstudiantes disponibles:")
            print(sistema.listar_estudiantes())
            
            estudiante_id = input("\nIngrese el ID del estudiante: ")
            curso_id = input("Ingrese el código del curso (dejar vacío para promedio general): ")
            curso_id = curso_id if curso_id else None
            
            promedio = sistema.obtener_promedio_estudiante(estudiante_id, curso_id)
            if promedio is not None:
                print(f"Promedio del estudiante: {promedio:.2f}")
            else:
                print("No se encontraron calificaciones para el estudiante.")
                
        elif opcion == "8":
            os.system('cls')
            curso_id = input("Ingrese el código del curso (dejar vacío para todos los cursos): ")
            curso_id = curso_id if curso_id else None
            limite = int(input("Ingrese el límite de promedio (default 60): ") or 60)
            
            estudiantes_bajo = sistema.estudiantes_promedio_bajo(curso_id, limite)
            if estudiantes_bajo:
                print("\nEstudiantes con promedio bajo:")
                for est, prom in estudiantes_bajo:
                    print(f"  {est.nombre} - Promedio: {prom:.2f}")
            else:
                print("No hay estudiantes con promedio bajo.")
                
        elif opcion == "9":
            os.system('cls')
            curso_id = input("Ingrese el código del curso (dejar vacío para todos los cursos): ")
            curso_id = curso_id if curso_id else None
            limite = int(input("Ingrese el límite de promedio (default 90): ") or 90)
            
            estudiantes_alto = sistema.estudiantes_promedio_alto(curso_id, limite)
            if estudiantes_alto:
                print("\nEstudiantes con promedio alto:")
                for est, prom in estudiantes_alto:
                    print(f"  {est.nombre} - Promedio: {prom:.2f}")
            else:
                print("No hay estudiantes con promedio alto.")
                
        elif opcion == "10":
            os.system('cls')
            print("\nCursos registrados:")
            print(sistema.listar_cursos())
            
        elif opcion == "11":
            os.system('cls')
            print("\nEstudiantes registrados:")
            print(sistema.listar_estudiantes())
            
        elif opcion == "12":
            os.system('cls')
            print("\nCursos disponibles:")
            print(sistema.listar_cursos())
            
            curso_id = input("\nIngrese el código del curso: ")
            print(f"\nEvaluaciones del curso {curso_id}:")
            print(sistema.listar_evaluaciones_curso(curso_id))
            
        elif opcion == "13":
            os.system('cls')
            print("\nProfesores registrados:")
            print(sistema.listar_profesores())
        
        elif opcion == "14":
            os.system('cls')
            print("\nCursos disponibles:")
            print(sistema.listar_cursos())
            curso_id = input("\nIngrese el código del curso: ")
            print(f"\nEstudiantes inscritos en el curso {curso_id}:")
            print(sistema.listar_estudiantes_curso(curso_id))
                
        elif opcion == "0":
            os.system('cls')
            print("Saliendo del sistema. ¡Hasta pronto!")
            break
            
        else:
            os.system('cls')
            print("Opción no válida. Por favor, seleccione una opción válida.")
        
        input("\nPresione Enter para continuar...")

menu()
