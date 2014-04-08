# -*- coding: utf-8 -*-
"""
/***************************************************************************
 FormationDialog
                                 A QGIS plugin
 Formation au développement de plugins
                             -------------------
        begin                : 2014-02-27
        copyright            : (C) 2014 by Arnaud Morvan
        email                : arnaud.morvan@camptocamp.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4 import QtCore, QtGui
from ui_metadata import Ui_Metadata
# create the dialog for zoom to point

from qgis.core import QgsMapLayer, QgsVectorLayer


class MetadataDock(QtGui.QDockWidget, Ui_Metadata):

    iface = None

    layer = None

    def __init__(self, iface):
        QtGui.QDockWidget.__init__(self, iface.mainWindow())
        # Set up the user interface from Designer.
        # After setupUI you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)

        self.iface = iface
        self.update()
        self.iface.currentLayerChanged.connect(self.update)

    def update(self, layer=None):
        self.clear()

        layer = self.iface.activeLayer()
        if layer is None:
            return

        if isinstance(layer, QgsVectorLayer):
            self.rowCount.setText(str(layer.pendingFeatureCount()))
            self.colCount.setText(str(len(layer.dataProvider().fields())))

        if isinstance(layer, QgsMapLayer):
            self.crsName.setText(layer.crs().description())

    def clear(self):
        self.rowCount.setText('')
        self.colCount.setText('')
        self.crsName.setText('')
