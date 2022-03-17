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

def agregarTextura(textura):
    bpy.ops.material.new()
    
    if textura == 'Negro':
        bpy.data.materials["Material.001"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.00103149, 0.00103149, 0.00103149, 1)
    elif textura == 'Blanco':
        #bpy.data.materials["Material.002"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0.8, 0.8, 0.8, 1)
        bpy.data.materials["Material.002"].node_tree.nodes["Principled BSDF"].inputs[4].default_value = 0.5

    
def agregarLuzPuntual():
    bpy.ops.object.light_add(type='POINT', location=(9, 1.5, 13))
    bpy.context.object.data.energy = 100

def agregarCamara():
    bpy.ops.object.camera_add(enter_editmode=False, align='VIEW', location=(33.316, -25.028, 22.609), rotation=(1.1781, 0.0872665, 0.872665))


def agregarColor(r, g, b):
    activeObject = bpy.context.active_object
    mat = bpy.data.materials.new("")
    activeObject.data.materials.append(mat)
    bpy.context.object.active_material.diffuse_color = (r, g, b, 1)

def agregarTextura(metallic, roughless):
    bpy.context.object.active_material.metallic = metallic
    bpy.context.object.active_material.roughness = roughless
    

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
    
    def crearCilindro(objName, verticeNum):
        bpy.ops.mesh.primitive_cylinder_add(vertices=verticeNum, radius=1, depth=2, enter_editmode=False, location=(0, 0, 0))
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
        
    def escalar():
        activarDesactivarModoEditar()
        bpy.ops.transform.resize(value=(0.644061, 1, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), 
                                orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, 
                                use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, 
                                use_proportional_connected=False, use_proportional_projected=False, release_confirm=True)
        activarDesactivarModoEditar()


'''*************************'''
'''Clase para crear robot'''
'''*************************'''

class Robot:
    def crearBase():
        Objeto.crearCubo('BaseRectangular')
        Seleccionado.escalar((8.6, 8.4, 0.55))
        Editar.biselar(0.05, 0, 10)
        
        Objeto.crearCilindro('BaseCilindrica', 64)
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
        agregarColor(1,1,1)
        agregarTextura(0.5,0.0)
        
    
    def crearLink1():
        Objeto.crearCilindro('CapaConectora', 64)
        Activo.escalar((2.1, 2.1, 0.04))
        Activo.posicionar((0, 0, 3.7))
        
        
        Objeto.crearCilindro('BaseCilindrica', 64)
        Activo.escalar((2.4, 2.4, 0.3))
        Activo.posicionar((0, 0, 4))
        Editar.biselar(0.1, 0, 10)
        
        
        Objeto.crearCubo('Cuello')
        Activo.escalar((5.5, 4, 5))
        Editar.biselar(0.07, 0, 10)
        Activo.posicionar((0, 0, 5))
        
        Objeto.crearCilindro('CilindroExterno', 64)
        Activo.escalar((1.4, 1.4, 1.35))
        Activo.posicionar((0, -0.1, 6))
        Activo.rotar((3.1415 / 2, 0, 0))
        
        Objeto.crearCilindro('CillindroInterno', 64)
        Activo.escalar((1.22, 1.22, 0.14))
        Activo.posicionar((0, 1.25, 6))
        Activo.rotar((3.1415 / 2, 0, 0))
        
        # Juntar todas las piezas del link1
        juntarObjetos(['CapaConectora', 'BaseCilindrica','Cuello','CilindroExterno','CillindroInterno'])
        Activo.renombrar('Link1')
        agregarColor(1,1,1)
        agregarTextura(0.5,0.0)
    

    def crearLink2():
        # Brazo 1 (derecho)
        Objeto.crearCilindro('ParteSuperiorBrazo', 64)
        Activo.escalar((1.125, 1.125, 0.6))
        Activo.posicionar((0, 0, 13.8))
        Activo.rotar((3.1415 / 2, 0, 0))
        
        Objeto.crearCubo('cuerpoBrazo')
        Activo.escalar((7, 2.4, 9.6))
        Activo.posicionar((0, 0, 11.5))
        Editar.escalar()
        
        Objeto.crearCilindro('ParteInferiorBrazo', 64)
        Activo.escalar((1.6, 1.6, 0.6))
        Activo.posicionar((0, 0, 9))
        Activo.rotar((3.1415 / 2, 0, 0))
        
        juntarObjetos(['ParteInferiorBrazo', 'cuerpoBrazo','ParteSuperiorBrazo'])
        Activo.renombrar('Brazo1')
        Activo.escalar((1.6, 1.6, 0.5))
        Activo.posicionar((0, 1.9, 9))
        Editar.biselar(0.1, 0, 10)
        
        # Brazo 2 (izquierdo)
        Objeto.crearCilindro('ParteSuperiorBrazo', 64)
        Activo.escalar((1.125, 1.125, 0.6))
        Activo.posicionar((0, 0, 13.8))
        Activo.rotar((3.1415 / 2, 0, 0))
        
        Objeto.crearCubo('cuerpoBrazo')
        Activo.escalar((7, 2.4, 9.6))
        Activo.posicionar((0, 0, 11.5))
        Editar.escalar()
        
        Objeto.crearCilindro('ParteInferiorBrazo', 64)
        Activo.escalar((1.6, 1.6, 0.6))
        Activo.posicionar((0, 0, 9))
        Activo.rotar((3.1415 / 2, 0, 0))
        
        juntarObjetos(['ParteInferiorBrazo', 'cuerpoBrazo','ParteSuperiorBrazo'])
        Activo.renombrar('CuerpoBrazo2')
        Activo.escalar((1.6, 1.6, 0.5))
        Activo.posicionar((0, -1.9, 9))
        Editar.biselar(0.1, 0, 10)
        
        Objeto.crearCilindro('PiezaLateralCilindrica', 64)
        Activo.escalar((1, 1, 0.15))
        Activo.posicionar((0, -1.4, 13.8))
        Activo.rotar((3.1415 / 2, 0, 0))
        
        juntarObjetos(['CuerpoBrazo2', 'PiezaLateralCilindrica'])
        Activo.renombrar('Brazo2')
        
        # Conector
        Objeto.crearCubo('PiezaCentral')
        Activo.escalar((2.5, 6, 2.5))
        Activo.posicionar((0, 0, 11.5))
        Editar.biselar(0.09, 0, 10)
        
        Objeto.crearCubo('PiezaLateral1')
        Activo.escalar((3, 1.1, 3))
        Activo.posicionar((0, -1.4, 11.5))
        Editar.biselar(0.06, 0, 10)
        
        Objeto.crearCubo('PiezaLateral2')
        Activo.escalar((3, 1.1, 3))
        Activo.posicionar((0, 1.4, 11.5))
        Editar.biselar(0.06, 0, 10)
        
        juntarObjetos(['PiezaCentral', 'PiezaLateral1', 'PiezaLateral2'])
        Activo.renombrar('ConectorCentral')
        Activo.posicionar((0.15, 1.4, 11.4))
        
        
        # Juntar todas las piezas del link2
        juntarObjetos(['Brazo1', 'Brazo2','ConectorCentral'])
        Activo.renombrar('Link2')
        agregarColor(1,1,1)
        agregarTextura(0.5,0.0)
        
        
    def crearLink3():
        # Parte inferior que conectar el link3 con el link2
        Objeto.crearCilindro('CilindroFuera', 64)
        Activo.escalar((1.125, 1.125, 1.28))
        Activo.posicionar((0, 0.08, 17))
        Activo.rotar((3.1415 / 2, 0, 0))
        
        Objeto.crearCilindro('CilindroDentro', 64)
        Activo.escalar((0.85, 0.85, 1.33))
        Activo.posicionar((0, 0.1, 17))
        Activo.rotar((3.1415 / 2, 0, 0))

        
        Objeto.crearCilindro('CilindroGrande', 14)
        Activo.escalar((1.6, 1.6, 1.15))
        Activo.posicionar((-0.35, -0.05, 18))
        Activo.rotar((3.1415 / 2, 0, 0))
        
        Objeto.crearCubo('CuboResta')
        Activo.escalar((10, 6, 5))
        Activo.posicionar((-0.5, 0, 19.6))
        Activo.rotar((0, 3.1415 / -8, 0))
        
        diferencia('CilindroGrande', 'CuboResta')
        Editar.biselar(0.09, 0, 10)
        

        # Cuerpo del link3
        ## Parte inferior: octagono recortado
        Objeto.crearCilindro('OctagonoBase', 8)
        Activo.escalar((1.245, 1.245, 1))
        Activo.posicionar((1.25, -0.05, 18))
        Activo.rotar((3.1415 / -2, 3.1415 * 2.625, 3.1415 / -2))
        Editar.biselar(0.1, 0, 10)
        
        Objeto.crearCubo('CuboResta')
        Activo.escalar((13, 6, 5))
        Activo.posicionar((-0.5, 0, 19.6))
        Activo.rotar((0, 3.1415 / -8, 0))
        
        diferencia('OctagonoBase', 'CuboResta')

        # Parte externa: cubo recortado
        Objeto.crearCubo('CuboExterno')
        Activo.escalar((8, 4.61, 5.5))
        Activo.posicionar((0.25, -0.05, 18.9))
        
        Objeto.crearCubo('CuboResta')
        Activo.escalar((13, 6, 5))
        Activo.posicionar((-0.5, -0.1, 19.6))
        Activo.rotar((0, 3.1415 / -8, 0))
        
        diferencia('CuboExterno', 'CuboResta')
        Editar.biselar(0.02, 0, 6)
        
        juntarObjetos(['CilindroFuera', 'CilindroDentro', 'CilindroGrande', 'OctagonoBase', 'CuboExterno'])
        Activo.renombrar('CapaExterna')
        
        ## Parte interna: cilindro recortado + cubo
        Objeto.crearCilindro('CilindroCuboInterno', 36)
        Activo.escalar((1, 1.5, 0.885))
        Activo.posicionar((-0.98, -0.05, 18.644))
        Activo.rotar((3.1415 / 2, 0, 0))
        
        Objeto.crearCubo('CuboResta')
        Activo.escalar((6, 6, 5))
        Activo.posicionar((-0.5, -0.1, 20.835))
        
        diferencia('CilindroCuboInterno', 'CuboResta')
        
        Objeto.crearCubo('CuboInterno')
        Activo.escalar((7.5, 3.541, 3.434))
        Activo.posicionar((0.12214, -0.053072, 18.731))
        
        juntarObjetos(['CilindroCuboInterno', 'CuboInterno'])
        Editar.biselar(0.04, 0, 6)
        
        
        # Parte delantera que permite conectar el link3 con el link4
        Objeto.crearCilindro('Conector', 64)
        Activo.escalar((1.12, 1.12, 1))
        Activo.posicionar((2.0391, -0.05118, 18.038))
        Activo.rotar((0, 3.1415 / 2, 0))
        
        # Juntar todas las piezas de link3
        juntarObjetos(['CapaExterna', 'CuboInterno', 'Conector'])
        Activo.renombrar('Link3')
        agregarColor(1,1,1)
        agregarTextura(0.5,0.0)
    
    
    def crearLink4():
        # Parte que permite conectar link4 con link3
        Objeto.crearCilindro('ConectorALink3', 64)
        Activo.escalar((0.7, 0.7, 0.3))
        Activo.posicionar((4, -0.05118, 18.038))
        Activo.rotar((0, 3.1415 / 2, 0))
        
        
        # Cuerpo del link4
        Objeto.crearCubo('CuerpoRectangular')
        Activo.escalar((6, 5, 3.434))
        Activo.posicionar((5.5, -0.053072, 18.067))

        Objeto.crearCubo('CuboResta')
        Activo.escalar((5, 3, 5))
        Activo.posicionar((6.6, -0.053072, 18))
        
        diferencia('CuerpoRectangular', 'CuboResta')
    
    
        # Parte que permite conectar link4 con link5
        Objeto.crearCilindro('ConectorALink5', 64)
        Activo.escalar((0.858, 0.858, 1.253))
        Activo.posicionar((6.8797, -0.05118, 18.0675))
        Activo.rotar((3.1415 / 2, 0, 0))
        
        Objeto.crearCubo('CuboResta')
        Activo.escalar((5, 2.7, 5))
        Activo.posicionar((7.15, -0.053072, 18))
        
        diferencia('ConectorALink5', 'CuboResta')
        
        
        # Juntar todas las piezas de link4
        juntarObjetos(['CuerpoRectangular', 'ConectorALink5'])
        Activo.renombrar('CuerpoLink4')
        Editar.biselar(0.09, 0, 6)
        juntarObjetos(['ConectorALink3', 'CuerpoLink4'])
        Activo.renombrar('Link4')
        agregarColor(1,1,1)
        agregarTextura(0.5,0.0)
        
        
    def crearLink5():
        # Cuerpo 
        Objeto.crearCubo('PiezaTrasera')
        Activo.escalar((2.8, 2.6, 3))
        Activo.posicionar((9.5, -0.052, 18.067))
        Editar.biselar(0.09, 0, 6)
        
        Objeto.crearCilindro('ConectorALink4', 64)
        Activo.escalar((0.95, 0.858, 0.65))
        Activo.posicionar((10, -0.05118, 18.0675))
        Activo.rotar((3.1415 / 2, 0, 0))
        
        Objeto.crearCubo('CuboResta')
        Activo.escalar((3, 4, 5))
        Activo.posicionar((9, -0.053072, 18))
        
        diferencia('ConectorALink4', 'CuboResta')
        
        Objeto.crearCilindro('CilindroCuerpo', 64)
        Activo.escalar((0.65, 0.65, 0.3))
        Activo.posicionar((10.87, -0.05118, 18.0675))
        Activo.rotar((0, 3.1415 / 2, 0))
        
        juntarObjetos(['PiezaTrasera', 'ConectorALink4', 'CilindroCuerpo'])
        Activo.renombrar('Pieza1')
        agregarColor(1,1,1)
        agregarTextura(0.5,0.0)
        
        # Cabeza
        Objeto.crearCilindro('CilindroExterno', 64)
        Activo.escalar((0.59, 0.59, 0.2))
        Activo.posicionar((11.333, -0.05118, 18.0675))
        Activo.rotar((0, 3.1415 / 2, 0))

        Objeto.crearCilindro('CilindroResta', 64)
        Activo.escalar((0.35, 0.35, 0.1))
        Activo.posicionar((11.529, -0.05118, 18.0675))
        Activo.rotar((0, 3.1415 / 2, 0))
        
        diferencia('CilindroExterno', 'CilindroResta')
        
        Objeto.crearCilindro('CilindroInterno', 64)
        Activo.escalar((0.5, 0.5, 0.2))
        Activo.posicionar((11.4, -0.05118, 18.0675))
        Activo.rotar((0, 3.1415 / 2, 0))
        
        Objeto.crearCilindro('CilindroResta', 64)
        Activo.escalar((0.35, 0.35, 0.3))
        Activo.posicionar((11.529, -0.05118, 18.0675))
        Activo.rotar((0, 3.1415 / 2, 0))
        
        diferencia('CilindroInterno', 'CilindroResta')
        juntarObjetos(['CilindroExterno','CilindroInterno'])
        Activo.renombrar('Pieza2')
        agregarColor(0,0,0)
        agregarTextura(0.3,0.3)
        
        # Juntar todas las piezas de link5
        juntarObjetos(['Pieza1', 'Pieza2'])
        Activo.renombrar('Link5')


        
        
    def crearLink6():
        Objeto.crearCilindro('Link6', 64)
        Activo.escalar((0.35, 0.35, 0.15))
        Activo.posicionar((12, -0.05118, 18.0675))
        Activo.rotar((0, 3.1415 / 2, 0))
        
        Objeto.crearCilindro('CilindroRestaCentral', 64)
        Activo.escalar((0.2, 0.2, 0.1))
        Activo.posicionar((12.1, -0.05118, 18.0675))
        Activo.rotar((0, 3.1415 / 2, 0))
        
        Objeto.crearCilindro('CilindroRestaLateral1', 64)
        Activo.escalar((0.04, 0.04, 0.1))
        Activo.posicionar((12.055, -0.05118, 18.336))
        Activo.rotar((0, 3.1415 / 2, 0))
        
        Objeto.crearCilindro('CilindroRestaLateral2', 64)
        Activo.escalar((0.04, 0.04, 0.1))
        Activo.posicionar((12.055, -0.05118, 17.799))
        Activo.rotar((0, 3.1415 / 2, 0))
        
        Objeto.crearCilindro('CilindroRestaLateral3', 64)
        Activo.escalar((0.04, 0.04, 0.1))
        Activo.posicionar((12.055, -0.32151, 18.0675))
        Activo.rotar((0, 3.1415 / 2, 0))
        
        Objeto.crearCilindro('CilindroRestaLateral4', 64)
        Activo.escalar((0.04, 0.04, 0.1))
        Activo.posicionar((12.055, 0.21915, 18.0675))
        Activo.rotar((0, 3.1415 / 2, 0))
        
        diferencia('Link6', 'CilindroRestaCentral')
        diferencia('Link6', 'CilindroRestaLateral1')
        diferencia('Link6', 'CilindroRestaLateral2')
        diferencia('Link6', 'CilindroRestaLateral3')
        diferencia('Link6', 'CilindroRestaLateral4')
        
        agregarColor(0.08, 0.08, 0.08)
        agregarTextura(0.5, 0.3)
    
    
    def montar():
        seleccionarObjeto('Link1')
        Activo.posicionar((0, 1.21, 5.4505))
        
        seleccionarObjeto('Link2')
        Activo.posicionar((0.15, 1.4, 8))
        
        seleccionarObjeto('Link3')
        Activo.posicionar((2.0391, -0.05118, 11.526))
        
        seleccionarObjeto('Link4')
        Activo.posicionar((6.2133, -0.05118, 11.526))
        
        seleccionarObjeto('Link5')
        Activo.posicionar((7.43569, -0.05118, 11.526))
        
        seleccionarObjeto('Link6')
        Activo.posicionar((7.63965, -0.05118, 11.526))
        
        
        
'''************'''
''' M  A  I  N '''
'''************'''
if __name__ == "__main__":
    # Limpiar escena
    borrarObjetos()
    
    agregarLuzPuntual()
    agregarCamara()
    
    Robot.crearBase()
    Robot.crearLink1()
    Activo.posicionar((0, 1.21, 5.4505))
    Robot.crearLink2()
    Activo.posicionar((0.15, 1.4, 8))
    Robot.crearLink3()
    Activo.posicionar((2.0391, -0.05118, 11.526))
    Robot.crearLink4()
    Activo.posicionar((6.2133, -0.05118, 11.526))
    Robot.crearLink5()
    Activo.posicionar((7.43569, -0.05118, 11.526))
    Robot.crearLink6()
    Activo.posicionar((7.63965, -0.05118, 11.526))
    
    #Robot.montar()
    
    

    
    

    