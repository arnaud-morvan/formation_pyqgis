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
 This script initializes the plugin, making it known to QGIS.
"""

'''
import sys
sys.path.append("/home/amorvan/.eclipse/org.eclipse.platform_3.8_155965261"
    "/plugins/org.python.pydev_3.0.0.201311051910/pysrc/")
import pydevd
pydevd.settrace()
'''

def classFactory(iface):
    # load Formation class from file Formation
    from formation_plugin import FormationPlugin
    return FormationPlugin(iface)
