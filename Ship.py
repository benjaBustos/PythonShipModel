import glfw
from OpenGL.GL import *
import OpenGL.GL.shaders
import numpy as np
import sys

import Creacion as cr
import easy_shaders as es
import scene_graph2 as sg
import transformations2 as tr2


class Controller:
    def __init__(self):
        self.fillPolygon = True
        self.showAxis = True
        self.view = 1


# we will use the global controller as communication with the callback function
controller = Controller()


def on_key(window, key, scancode, action, mods):
    if action != glfw.PRESS:
        return

    global controller

    if key == glfw.KEY_SPACE:
        controller.fillPolygon = not controller.fillPolygon

    elif key == glfw.KEY_LEFT_CONTROL:
        controller.showAxis = not controller.showAxis

    elif key == glfw.KEY_1:
        controller.view = 1

    elif key == glfw.KEY_2:
        controller.view = 2

    elif key == glfw.KEY_3:
        controller.view = 3

    elif key == glfw.KEY_4:
        controller.view = 4

    elif key == glfw.KEY_ESCAPE:
        sys.exit()

    else:
        print('Unknown key')

def crearbarco(image_filename_1,image_filename_2,image_filename_3):
    gpuBote = es.toGPUShape(cr.createBote(image_filename_1), GL_REPEAT, GL_LINEAR)
    gpuMastil = es.toGPUShape(cr.createMastil(image_filename_1), GL_REPEAT, GL_LINEAR)
    gpuVela = es.toGPUShape(cr.createVela(image_filename_2),GL_REPEAT, GL_LINEAR)
    gpuFlag = es.toGPUShape(cr.createFlag(image_filename_3),GL_REPEAT, GL_LINEAR)

    #instancia del bote
    bote = sg.SceneGraphNode("bote")
    bote.childs +=[gpuBote]
    #instancia de flag
    flag = sg.SceneGraphNode("flag")
    flag.transform = tr2.uniformScale(0.5)
    flag.childs +=[gpuFlag]

    flagTranslate = sg.SceneGraphNode("flagTranslate")
    flagTranslate.transform = tr2.translate(-3,0,2.5)
    flagTranslate.childs += [flag]
    #2 instancias de mastil
    frontMastil = sg.SceneGraphNode("frontMastil")
    frontMastil.transform = tr2.translate(1.2,0,0)
    frontMastil.childs +=[gpuMastil]

    backMastil = sg.SceneGraphNode("backMastil")
    backMastil.transform = tr2.translate(-1.2,0,0)
    backMastil.childs += [gpuMastil]
    #2 instancias de velas
    frontVela = sg.SceneGraphNode("frontVela")
    frontVela.transform = tr2.translate(1.2,0,2.5)
    frontVela.childs += [gpuVela]

    backVela = sg.SceneGraphNode("backVela")
    backVela.transform = tr2.translate(-1.2,0,2.5)
    backVela.childs += [gpuVela]
    #instancia de cola
    cola = sg.SceneGraphNode("cola")
    cola.transform = tr2.uniformScale(0.5)
    cola.childs += [gpuMastil]
    colaTranslated = sg.SceneGraphNode("colaTranslated")
    colaTranslated.transform = tr2.translate(-2.5,0,1)
    colaTranslated.childs += [cola]

    #instacia del barco completo
    barco = sg.SceneGraphNode("barco")
    barco.childs +=[bote]
    barco.childs +=[frontMastil]
    barco.childs +=[backMastil]
    barco.childs +=[colaTranslated]
    barco.childs += [frontVela]
    barco.childs += [backVela]
    barco.childs += [flagTranslate]

    #barco rotado
    scaledBarco = sg.SceneGraphNode("scaledBarco")
    scaledBarco.transform = tr2.uniformScale(0.05)
    scaledBarco.childs +=[barco]
    rotatedBarco = sg.SceneGraphNode("rotatedBarco")
    rotatedBarco.transform = tr2.rotationZ(3)
    rotatedBarco.childs +=[scaledBarco]

    traslatedBarco = sg.SceneGraphNode("traslatedBarco")
    traslatedBarco.transform = tr2.translate(0.0,0.0,0.0)
    traslatedBarco.childs += [rotatedBarco]
    return traslatedBarco
def crearIsla():
    gpuIsla = es.toGPUShape(cr.createIsland())
    isla = sg.SceneGraphNode("isla")
    isla.childs +=[gpuIsla]
    return isla
def createMar(image_filename):
    gpuMar = es.toGPUShape(cr.createSuperficie(image_filename,1,1), GL_REPEAT, GL_LINEAR)
    mar =  sg.SceneGraphNode("mar")
    mar.childs += [gpuMar]
    return mar
if __name__ == "__main__":
    if not glfw.init():
        sys.exit()
    width = 1280
    height = 800

    window = glfw.create_window(width,height,"Tarea 2", None, None)
    if not window:
        glfw.terminate()
        sys.exit()
    glfw.make_context_current(window)
    glfw.set_key_callback(window, on_key)
    mvcPipeline = es.SimpleModelViewProjectionShaderProgram()
    textureShaderProgram = es.SimpleTextureModelViewProjectionShaderProgram()

    glClearColor(0.07, 0.21, 0.66, 1.0)
    glEnable(GL_DEPTH_TEST)
    gpuAxis = es.toGPUShape(cr.createAxis(1))
    mar = createMar("water.jpg")
    barco = crearbarco("wood.jpg","sail.jpg","sail.jpg")
    isla = crearIsla()
    #projection = tr2.perspective(200, float(width) / float(height), 0.1, 100)
    #projection = tr2.frustum(-1, 1,-1, 1, 10, 1000)
    projection = tr2.ortho(-1, 1, -1, 1, 0.1, 1000)

    while not glfw.window_should_close(window):
        # Using GLFW to check for input events
        glfw.poll_events()

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        if (controller.fillPolygon):
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)



        if controller.view == 1:
            view = tr2.lookAt(
                np.array([0, 9, 7]),
                np.array([0, 0, 0]),
                np.array([0, 0, 1])
            )
        elif controller.view == 2:
            view = tr2.lookAt(
                np.array([8, -6, 3]),
                np.array([0, 0, 0]),
                np.array([0, 0, 1])
            )
        elif controller.view == 3:
            view = tr2.lookAt(
                np.array([10, 5, 1]),
                np.array([0, 0, 0]),
                np.array([0, 0, 1])
            )
        elif controller.view == 4:
            view = tr2.lookAt(
                np.array([10, 5, 0]),
                np.array([0, 0, 0]),
                np.array([0, 0, 1])
            )
        if controller.showAxis:
            glUseProgram(mvcPipeline.shaderProgram)
            glUniformMatrix4fv(glGetUniformLocation(mvcPipeline.shaderProgram, "projection"), 1, GL_TRUE, projection)
            glUniformMatrix4fv(glGetUniformLocation(mvcPipeline.shaderProgram, "view"), 1, GL_TRUE, view)
            glUniformMatrix4fv(glGetUniformLocation(mvcPipeline.shaderProgram, "model"), 1, GL_TRUE, tr2.identity())
            mvcPipeline.drawShape(gpuAxis, GL_LINES)

        glUseProgram(textureShaderProgram.shaderProgram)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "projection"), 1, GL_TRUE,
                           projection)
        glUniformMatrix4fv(glGetUniformLocation(textureShaderProgram.shaderProgram, "view"), 1, GL_TRUE, view)
        #sg.drawSceneGraphNode(mar, textureShaderProgram)
        sg.drawSceneGraphNode(barco, textureShaderProgram)
        #sg.drawSceneGraphNode(isla, mvcPipeline)
        glfw.swap_buffers(window)
    glfw.terminate()