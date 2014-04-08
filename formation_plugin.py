# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Formation
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import QgsMessageBar

# Initialize Qt resources from file resources.py
import resources_rc

# Import the code for the dialog
from formation_dialog import FormationDialog
from metadata_dock import MetadataDock
import os.path


class FormationPlugin(QObject):

    menu = u"&Formation"

    metadataDock = None

    def __init__(self, iface):
        """Constructor for the plugin.

        :param iface: A QGisAppInterface instance we use to access QGIS via.
        :type iface: QgsAppInterface
        """
        super(FormationPlugin, self).__init__()

        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # initialize locale
        locale = QSettings().value("locale/userLocale")[0:2]
        localePath = os.path.join(self.plugin_dir, 'i18n', 'formation_{}.qm'.format(locale))

        if os.path.exists(localePath):
            self.translator = QTranslator()
            self.translator.load(localePath)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

    def initGui(self):
        self.pointAction = QAction(
            self.tr("Saisir un point"),
            self.iface.mainWindow())
        self.pointAction.triggered.connect(self.showPointDialog)

        self.iface.addPluginToMenu(self.menu, self.pointAction)
        self.iface.addToolBarIcon(self.pointAction)

        self.metadataAction = QAction(
            self.tr("Layer metadata"),
            self.iface.mainWindow())
        self.metadataAction.setCheckable(True)
        self.metadataAction.toggled.connect(self.toggleMetadata)

        self.iface.addPluginToMenu(self.menu, self.metadataAction)
        self.iface.addToolBarIcon(self.metadataAction)

    def unload(self):
        self.iface.removePluginMenu(self.menu, self.pointAction)
        self.iface.removeToolBarIcon(self.pointAction)

        self.iface.removePluginMenu(self.menu, self.metadataAction)
        self.iface.removeToolBarIcon(self.metadataAction)

    def toggleMetadata(self, checked):
        if checked:
            if self.metadataDock is None and self.iface:
                self.metadataDock = MetadataDock(self.iface)

                # try to restore position from stored main window state
                if not self.iface.mainWindow().restoreDockWidget(self.metadataDock):
                    self.iface.addDockWidget(Qt.LeftDockWidgetArea, self.metadataDock)
                self.metadataDock.hide()

            self.metadataDock.show()
            self.metadataDock.raise_()

        else:
            self.metadataDock.hide()

    def showPointDialog(self):
        dlg = FormationDialog()
        dlg.show()
        result = dlg.exec_()

        # Si le bouton OK a été pressé
        if result == 1:
            # do something useful (delete the line containing pass and
            # substitute with your code)

            x = dlg.XBox.value()
            y = dlg.YBox.value()
            point = QgsPoint(x, y)


            mapExtent = self.iface.mapCanvas().fullExtent()

            if not mapExtent.contains(point):
                self.iface.messageBar().pushMessage(
                    self.tr('Saisir un point'),
                    self.tr('Le point est situé en dehors des limites de la carte'),
                    QgsMessageBar.WARNING,
                    5)
                return

            crs = self.iface.mapCanvas().mapRenderer().destinationCrs()
            print crs.authid()

            # "Point?crs=epsg:4326&field=id:integer&field=name:string(20)&index=yes"
            uri = 'Point?crs={}'.format(crs.authid())

            layer = QgsVectorLayer('Point', 'temp_layer', 'memory')
            pr = layer.dataProvider()

            '''
            # add fields
            pr.addAttributes( [ QgsField("name", QVariant.String),
                QgsField("age",  QVariant.Int),
                QgsField("size", QVariant.Double) ] )
            '''

            # add a feature
            fet = QgsFeature()
            fet.setGeometry(QgsGeometry.fromPoint(point))
            #fet.setAttributes(["Johny", 2, 0.3])
            pr.addFeatures([fet])

            # update layer's extent when new features have been added
            # because change of extent in provider is not propagated to the layer
            layer.updateExtents()

            symbol = QgsSymbolV2.defaultSymbol(layer.geometryType())
            symbol.setColor(QColor('#00ff80'))
            layer.rendererV2().setSymbol(symbol)

            QgsMapLayerRegistry.instance().addMapLayer(layer)
