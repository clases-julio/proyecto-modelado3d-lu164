import bpy

'''*********************************************************************'''
'''Funciones comunes útiles para selección/activación/borrado de objetos'''
'''*********************************************************************'''
def seleccionarObjeto(nombreObjeto): # Seleccionar un objeto por su nombre
    bpy.ops.object.select_all(action='DESELECT') # deseleccionamos todos...
    bpy.ops.object.select_pattern(pattern=nombreObjeto) # ...excepto el buscado
    
def activarObjeto(nombreObjeto): # Activar un objeto por su nombre
    bpy.ops.object.select_pattern(pattern=nombreObjeto)
    bpy.context.active_object.select_set(state=True)

def borrarObjeto(nombreObjeto): # Borrar un objeto por su nombre
    seleccionarObjeto(nombreObjeto)
    bpy.ops.object.delete(use_global=False)

def borrarObjetos(): # Borrar todos los objetos
    if(len(bpy.data.objects) != 0):
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.delete(use_global=False)

def seleccionarTodosObjetos():
    bpy.ops.object.select_all(action='SELECT')
    
def activarDesactivarModoEditar():
    bpy.ops.object.editmode_toggle()


def diferencia(objName, objNameTool):
    objeto = bpy.data.objects[objName]
    herramienta = bpy.data.objects[objNameTool]
    mod = objeto.modifiers.new("Boolean", type='BOOLEAN')
    mod.operation = 'DIFFERENCE'
    mod.object  = herramienta
    bpy.context.view_layer.objects.active = objeto
    
    bpy.ops.object.modifier_apply(apply_as='DATA', modifier=mod.name)
    bpy.data.objects.remove(herramienta)
    

def juntarObjetos(objetos):
    for objeto in objetos:
        activarObjeto(objeto)
    
    Seleccionado.juntar()




'''****************************************************************'''
'''Clase para realizar transformaciones sobre objetos seleccionados'''
'''****************************************************************'''
class Seleccionado:
    def mover(v):
        bpy.ops.transform.translate(
            value=v, constraint_axis=(True, True, True))

    def escalar(v):
        bpy.ops.transform.resize(value=v, constraint_axis=(True, True, True))

    def rotarX(v):
        bpy.ops.transform.rotate(value=v, orient_axis='X')

    def rotarY(v):
        bpy.ops.transform.rotate(value=v, orient_axis='Y')

    def rotarZ(v):
        bpy.ops.transform.rotate(value=v, orient_axis='Z')
    
    def juntar():
        bpy.ops.object.join()
    
    def copiarPegar():
        bpy.ops.view3d.pastebuffer()
        


'''**********************************************************'''
'''Clase para realizar transformaciones sobre objetos activos'''
'''**********************************************************'''
class Activo:
    def posicionar(v):
        bpy.context.object.location = v

    def escalar(v):
        bpy.context.object.scale = v

    def rotar(v):
        bpy.context.object.rotation_euler = v

    def renombrar(nombreObjeto):
        bpy.context.object.name = nombreObjeto

    def ocultarObjeto():
        bpy.context.object.hide_viewport = True

'''**************************************************************'''
'''Clase para realizar transformaciones sobre objetos específicos'''
'''**************************************************************'''
class Especifico:
    def escalar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].scale = v

    def posicionar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].location = v

    def rotar(nombreObjeto, v):
        bpy.data.objects[nombreObjeto].rotation_euler = v

'''************************'''
'''Clase para crear objetos'''
'''************************'''
class Objeto:
    def crearCubo(objName):
        bpy.ops.mesh.primitive_cube_add(size=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearEsfera(objName):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)

    def crearCono(objName):
        bpy.ops.mesh.primitive_cone_add(radius1=0.5, location=(0, 0, 0))
        Activo.renombrar(objName)
    
    def crearAro(objName):
        bpy.ops.mesh.primitive_torus_add(align='WORLD', location=(0, 0, 0), rotation=(0, 0, 0), major_radius=1, minor_radius=0.25, abso_major_rad=1.25, abso_minor_rad=0.75)
        Activo.renombrar(objName)
    
    def crearCilindro(objName):
        bpy.ops.mesh.primitive_cylinder_add(vertices=64, radius=1, depth=2, enter_editmode=False, location=(0, 0, 0))
        Activo.renombrar(objName)
    
'''*************************'''
'''Clase para editar objetos'''
'''*************************'''

class Editar:
    def biselar(offsetV, offsetPctV, segmentsV):
        activarDesactivarModoEditar()
        bpy.ops.mesh.bevel(offset=offsetV, offset_pct=offsetPctV, segments=segmentsV, release_confirm=True)
        #bpy.ops.mesh.bevel(offset=0.0106126, offset_pct=0, segments=10, release_confirm=True)
        activarDesactivarModoEditar()

    def inset():
        activarDesactivarModoEditar()
        #bpy.ops.mesh.shortest_path_pick(use_fill=False)
        #bpy.ops.mesh.shortest_path_pick(edge_mode='SELECT', use_fill=False, index=382)
        #bpy.ops.mesh.inset(thickness=0.448384, depth=0, release_confirm=False)
        bpy.ops.mesh.inset(thickness=0.448384, depth=0)
        bpy.ops.transform.translate(value=(0, 0, 0.299955), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', 
                                    constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', 
                                    proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
        
        activarDesactivarModoEditar()
        
    def escalar():
        activarDesactivarModoEditar()
        bpy.ops.transform.resize(value=(0.644061, 1, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
        activarDesactivarModoEditar()


'''************'''
''' M  A  I  N '''
'''************'''
if __name__ == "__main__":
    # Limpiar escena
    borrarObjetos()
    
    # ********   Creación de la base ********
    Objeto.crearCubo('BaseRectangular')
    Seleccionado.escalar((8.6, 8.4, 0.55))
    Editar.biselar(0.05, 0, 10)
    
    Objeto.crearCilindro('BaseCilindrica')
    Activo.escalar((2.1, 2.1, 1.6))
    Activo.posicionar((0, 0, 1.5))
    
    Objeto.crearCubo('CajaMotor')
    Seleccionado.escalar((3, 5, 5.6))
    Editar.biselar(0.02, 0, 10)
    Activo.posicionar((-2.2, 0, 1.38))
    
    Objeto.crearCubo('CajaMotor2')
    Seleccionado.escalar((3, 5, 5))
    Activo.posicionar((-3.4, 0, 1.26))
    
    # Juntar todas las piezas de la base
    seleccionarTodosObjetos()
    Seleccionado.juntar()
    Activo.renombrar('Base')
    
    #Seleccionado.ocultarObjeto()
    
    
    # ********  Creación del Link1 ************
    Objeto.crearCilindro('CapaConectora')
    Activo.escalar((2.1, 2.1, 0.04))
    Activo.posicionar((0, 0, 3.7))
    
    Objeto.crearCilindro('Base')
    Activo.escalar((2.4, 2.4, 0.3))
    Activo.posicionar((0, 0, 4))
    #Editar.inset()
    
    Objeto.crearCubo('Cuerpo')
    Activo.escalar((5.5, 4, 5))
    Editar.biselar(0.07, 0, 10)
    Activo.posicionar((0, 0, 5))
    
    Objeto.crearCilindro('Cabeza1')
    Activo.escalar((1.4, 1.4, 1.3))
    Activo.posicionar((0, -0.1, 6))
    Activo.rotar((3.1415 / 2, 0, 0))
    
    Objeto.crearCilindro('Cabeza2')
    Activo.escalar((1.22, 1.22, 0.14))
    Activo.posicionar((0, 1.21, 6))
    Activo.rotar((3.1415 / 2, 0, 0))
    
    juntarObjetos(['CapaConectora', 'Base','Cuerpo','Cabeza1','Cabeza2'])
    Activo.renombrar('Link1')
    
    
    # ********  Creación del Link2 ************
    
    # Brazo 1
    Objeto.crearCilindro('ParteInferiorBrazo')
    Activo.escalar((1.125, 1.125, 0.6))
    Activo.posicionar((0, 0, 13.8))
    Activo.rotar((3.1415 / 2, 0, 0))
    
    Objeto.crearCubo('cuerpoBrazo')
    Activo.escalar((7, 2.4, 9.6))
    Activo.posicionar((0, 0, 11.5))
    Editar.escalar()
    
    Objeto.crearCilindro('ParteSuperiorBrazo')
    Activo.escalar((1.6, 1.6, 0.6))
    Activo.posicionar((0, 0, 9))
    Activo.rotar((3.1415 / 2, 0, 0))
    
    juntarObjetos(['ParteInferiorBrazo', 'cuerpoBrazo','ParteSuperiorBrazo'])
    Activo.renombrar('Brazo1')
    Activo.escalar((1.6, 1.6, 0.5))
    Activo.posicionar((0, 1.9, 9))
    Editar.biselar(0.1, 0, 10)
    
    # Brazo 2
    Objeto.crearCilindro('ParteInferiorBrazo')
    Activo.escalar((1.125, 1.125, 0.6))
    Activo.posicionar((0, 0, 13.8))
    Activo.rotar((3.1415 / 2, 0, 0))
    
    Objeto.crearCubo('cuerpoBrazo')
    Activo.escalar((7, 2.4, 9.6))
    Activo.posicionar((0, 0, 11.5))
    Editar.escalar()
    
    Objeto.crearCilindro('ParteSuperiorBrazo')
    Activo.escalar((1.6, 1.6, 0.6))
    Activo.posicionar((0, 0, 9))
    Activo.rotar((3.1415 / 2, 0, 0))
    
    juntarObjetos(['ParteInferiorBrazo', 'cuerpoBrazo','ParteSuperiorBrazo'])
    Activo.renombrar('CuerpoBrazo2')
    Activo.escalar((1.6, 1.6, 0.5))
    Activo.posicionar((0, -1.9, 9))
    Editar.biselar(0.1, 0, 10)
    
    Objeto.crearCilindro('cilindroBrazo2')
    Activo.escalar((1, 1, 0.15))
    Activo.posicionar((0, -1.4, 13.8))
    Activo.rotar((3.1415 / 2, 0, 0))
    
    juntarObjetos(['CuerpoBrazo2', 'cilindroBrazo2'])
    Activo.renombrar('Brazo2')
    
    # Conector
    Objeto.crearCubo('Centro1')
    Activo.escalar((2.5, 6, 2.5))
    Activo.posicionar((0, 0, 11.5))
    Editar.biselar(0.09, 0, 10)
    
    Objeto.crearCubo('Aro1')
    Activo.escalar((3, 1.1, 3))
    Activo.posicionar((0, -1.4, 11.5))
    Editar.biselar(0.06, 0, 10)
    
    Objeto.crearCubo('Aro2')
    Activo.escalar((3, 1.1, 3))
    Activo.posicionar((0, 1.4, 11.5))
    Editar.biselar(0.06, 0, 10)
    
    juntarObjetos(['Centro1', 'Aro1', 'Aro2'])
    Activo.renombrar('ConectorCentral')
    Activo.posicionar((0.15, 1.4, 11.4))
    
    
    juntarObjetos(['Brazo1', 'Brazo2','ConectorCentral'])
    Activo.renombrar('Link2')
    
    
    # ********  Creación del Link3 ************
    
    Objeto.crearCubo('CajaExterior')
    Activo.escalar((8, 5, 5))
    Activo.posicionar((0, 0, 18))
    

    Objeto.crearCubo('CajaExteriorResta')
    Activo.escalar((10, 7, 5))
    Activo.posicionar((-0.5, 0, 19.3))
    Activo.rotar((0, 3.1415 / -8, 0))
    
    diferencia('CajaExterior', 'CajaExteriorResta')
    Editar.biselar(0.05, 0, 10)

    Objeto.crearCilindro('cilindroArticular')
    Activo.escalar((1.3, 1.3, 1.25))
    Activo.posicionar((-0.78, 0, 17.1))
    Activo.rotar((3.1415 / 2, 0, 0))
    Editar.biselar(0.09, 0, 10)
    
    Objeto.crearCubo('CajaExteriorResta')
    Activo.escalar((10, 6, 5))
    Activo.posicionar((-0.5, 0, 19.3))
    Activo.rotar((0, 3.1415 / -8, 0))
    
    diferencia('cilindroArticular', 'CajaExteriorResta')
    
    juntarObjetos(['CajaExterior', 'cilindroArticular'])
    Activo.renombrar('BaseLink3')

    Objeto.crearCubo('CajaInterior')
    Activo.escalar((7.4, 4.3, 4.3))
    Activo.posicionar((0.1, 0, 18))
    Editar.biselar(0.09, 0, 10)
    
    '''Objeto.crearCilindro('cilindroArticular')
    Activo.escalar((1, 1, 1))
    Activo.posicionar((-0.9, 0, 18))
    Activo.rotar((3.1415 / 2, 0, 0))
    Editar.biselar(0.09, 0, 10)'''
    
    
    Objeto.crearCilindro('boquilla')
    Activo.escalar((1, 1, 1.25))
    Activo.posicionar((1.5, 0, 17.8))
    Activo.rotar((0, 3.1415 / 2, 0))
    Editar.biselar(0.09, 0, 10)
    
    juntarObjetos(['BaseLink3', 'CajaInterior', 'boquilla'])
    
    

    
    

    
    
    
    
    
    
    
    
    
    
    

    