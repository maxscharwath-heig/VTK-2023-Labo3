#!/usr/bin/env python

# noinspection PyUnresolvedReferences
import vtkmodules.vtkInteractionStyle
# noinspection PyUnresolvedReferences
import vtkmodules.vtkRenderingOpenGL2
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOImage import vtkSLCReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer
)


def main():
    InputFilename = "vw_knee.slc"

    colors = vtkNamedColors()

    # vtkSLCReader to read.
    reader = vtkSLCReader()
    reader.SetFileName(InputFilename)
    reader.Update()

    # Create a mapper.
    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    contourFilter = vtkContourFilter()
    contourFilter.SetInputConnection(reader.GetOutputPort())
    contourFilter.SetValue(50, 72)
    # 50, 72

    outliner = vtkOutlineFilter()
    outliner.SetInputConnection(reader.GetOutputPort())
    outliner.Update()

    mapper = vtkPolyDataMapper()
    mapper.SetInputConnection(contourFilter.GetOutputPort())
    mapper.SetScalarVisibility(0)

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetDiffuse(0.8)
    actor.GetProperty().SetDiffuseColor(colors.GetColor3d('Ivory'))
    actor.GetProperty().SetSpecular(0.8)
    actor.GetProperty().SetSpecularPower(120.0)

    # Create a rendering window and renderer.
    renderer = vtkRenderer()
    renderWindow = vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(500, 500)

    # Create a renderwindowinteractor.
    renderWindowInteractor = vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    # Assign actor to the renderer.
    renderer.AddActor(actor)
    renderer.SetBackground(colors.GetColor3d('SlateGray'))

    # Pick a good view
    cam1 = renderer.GetActiveCamera()
    cam1.SetFocalPoint(0.0, 0.0, 0.0)
    cam1.SetPosition(0.0, -1.0, 0.0)
    cam1.SetViewUp(0.0, 0.0, -1.0)
    cam1.Azimuth(-90.0)
    renderer.ResetCamera()
    renderer.ResetCameraClippingRange()

    renderWindow.SetWindowName('ReadSLC')
    renderWindow.SetSize(640, 512)
    renderWindow.Render()

    # Enable user interface interactor.
    renderWindowInteractor.Initialize()
    renderWindow.Render()
    renderWindowInteractor.Start()


if __name__ == '__main__':
    main()