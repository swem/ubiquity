# -*- Mode: Python; coding: utf-8; indent-tabs-mode: nil; tab-width: 4 -*-
#
# Copyright (C) 2013
#
# Author: Daniel Chapman daniel@chapman-mail.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation; version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
from autopilot.input import Pointer, Mouse, Keyboard
from ubiquity_autopilot_tests.emulators import AutopilotGtkEmulatorBase, EmulatorException
from ubiquity_autopilot_tests.tools.compare import expectThat
from ubiquity_autopilot_tests.emulators.partconfig import Config1, Config2, Config3
from ubiquity_autopilot_tests.emulators.partconfig import Config4, Config5, Config6
from ubiquity_autopilot_tests.emulators import gtkcontrols, gtkaccessible, gtkcontainers
import time
import logging
logger = logging.getLogger(__name__)

custom_configs = [Config1, Config2, Config3, Config4, Config5, Config6]


class GtkWindow(AutopilotGtkEmulatorBase):
    """ Emulator class for a GtkWindow instance

        You should use this class for the main window of the application under test.
        By importing this into your test and select it as a property::

            from autopilotgtkemulators import gtktoplevel

            #and then in a property function
            class Test(AutopilotTestCase):

                def setUp():
                    ..........

                @property
                def main_window(self, ):
                    return self.app.select_single(gtktoplevel.GtkWindow)

        and now you can use self.main_window as our base for accessing all the objects within
        the Main application window.

        .. note:: When dealing with dialogs/windows spawned from the main application window
                  use the :func:`get_dialog` to get an object of the spawned dialog/window ::

                      >>> spawned_object = self.main_window.get_dialog('GtkDialog')

                  and you can use keyword arguments if it returns more than one::

                      >>> spawned_object = self.main_window.get_dialog('GtkDialog', name='foo')
    """
    def __init__(self, *args):

        super(GtkWindow, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())
        self.kbd = Keyboard.create()

    def get_dialog(self, dialogType, **kwargs):
        """ gets an object for a dialog window

                :param dialogType: Window type of the dialog e.g 'GtkDialog'
                :rtype: a dialog object of the given dialogType
                :raises: **EmulatorException** if a root instance cannot be obtained
                :raises: **ValueError** if the returned object is NoneType
        """
        logger.debug('Getting root instance')
        root = self.get_root_instance()
        if root is None:
            raise EmulatorException("Emulator could not get root instance")
        logger.debug(
            'Root instance received, Now selecting "{0}" object'.format(dialogType))
        dialog = root.select_single(dialogType, **kwargs)
        if dialog is None:
            raise ValueError(
                "Returned NoneType, could not select object of type {0}".format(dialogType))
        logger.debug('Returning {0} object'.format(dialogType))
        return dialog

    def run_install_progress_page_tests(self, ):
        ''' Runs the test for the installation progress page

            This method tracks the current progress of the install
            by using the fraction property of the progress bar
            to assertain the percentage complete.

        '''
        logger.debug("run_install_progress_page_tests()")
        #We cant assert page title here as its an external html page
        #Maybe try assert WebKitWebView is visible
        webkitwindow = self.select_single('GtkScrolledWindow',
                                          name='webkit_scrolled_window')
        expectThat(webkitwindow.visible).equals(
            True, msg="Expected the slideshow to be visible, but it wasn't")

        #Can we track the progress percentage?
        self.install_progress = self.select_single('GtkProgressBar',
                                                   name='install_progress')

    #Copying files progress bar
        self._track_install_progress_bar()

        self.install_progress.fraction.wait_for(0.0, timeout=120)
        #And now the install progress bar
        self._track_install_progress_bar()

    def _track_install_progress_bar(self):
        '''Gets the value of the fraction property of the progress bar

            so we can see when the progress bar is complete

        '''
        logger.debug("_track_install_progress_bar()")
        progress = 0.0
        complete = 1.0
        logger.debug('Percentage complete "{0:.0f}%"'.format(progress * 100))
        while progress < complete:
            #keep updating fraction value
            progress = self.install_progress.fraction
            # lets sleep for a second on each loop until we get near the end of the progress bar
            if progress < 0.7:
                time.sleep(1)

            logger.debug('Percentage complete "{0:.0f}%"'.format(progress * 100))
            #check for install errors while waiting
            try:
                crash_dialog = self.get_dialog('GtkDialog', BuilderName='crash_dialog')
                logger.debug("Checking crash dialog hasn't appeared....")
                if crash_dialog.visibe:
                    logger.error("Crash Dialog appeared")
                    assert not crash_dialog.visible, "Crash Dialog appeared! Something went wrong!!!"
                    progress = 1.0
            except Exception:
                pass
            # Lets try and grab the grub failed message box on the fly
            try:
                logger.debug("Checking failed grub install dialog hasn't appeared.......")
                grub_dialog = self.get_dialog('GtkMessageDialog')
                if grub_dialog.visible:
                    logger.error("The Grub installation failed dialog appeared :-(")
                    assert grub_dialog.visible != 1, "The Grub installation failed"
                    progress = 1.0
            except Exception:
                pass


class GtkDialog(GtkWindow):
    """ Emulator class for a GtkDialog, """
    def __init__(self, *args):
        super(GtkDialog, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())
        self.kbd = Keyboard.create()

    def set_partition_size(self, size=None):
        """ Sets the size of the partition being created

        :param size: Partition size in MB, if None will use rest of remaining space
        """
        logger.debug("set_partition_size({0})".format(str(size)))
        if size:
            spinbutton = self.select_single('GtkSpinButton',
                                            name='partition_size_spinbutton')
            spinbutton.enter_value(str(size))

        return

    def set_partition_location(self, locationKey):
        """ Sets the location of the partition being created

        :param locationKey: The location of the partition either;
                            - 'Beginning' or 'End'
        """

        logger.debug("set_partition_location({0})".format(locationKey))
        location_objects = {'Beginning': 'partition_create_place_beginning',
                            'End': 'partition_create_place_end'}
        location = location_objects[locationKey]
        radiobutton = self.select_single('GtkRadioButton',
                                         BuilderName=location)
        radiobutton.click()

    def set_partition_type(self, pType):
        """ Sets the partition type

        :param pType: The partition type, either 'Primary' or 'Logical'

        """
        logger.debug("set_partition_type({0})".format(pType))
        _partition_type = {'Primary': 'partition_create_type_primary',
                           'Logical': 'partition_create_type_logical'}
        part_type = _partition_type[pType]
        radiobutton = self.select_single('GtkRadioButton', BuilderName=part_type)
        radiobutton.click()

    def set_file_system_type(self, fsType):
        """ Sets the partitions file system type

        :param fsType: The required file sys type, choice from;
                       'Ext4', 'Ext3', 'Ext2', 'btrfs', 'JFS',
                       'XFS', 'Fat16', 'Fat32', 'ReiserFS', 'Swap'.
        """
        logger.debug("set_file_system_type({0})".format(fsType))
        _file_system_type = {'Ext4': 'Ext4 journaling file system',
                             'Ext3': 'Ext3 journaling file system',
                             'Ext2': 'Ext2 file system',
                             'btrfs': 'btrfs journaling file system',
                             'JFS': 'JFS journaling file system',
                             'XFS': 'XFS journaling file system',
                             'Fat16': 'Fat16 file system',
                             'Fat32': 'Fat32 file system',
                             'ReiserFS': 'ReiserFS journaling file system',
                             'Swap': 'swap area',
                             'Encrypt': '',
                             'Nothing': 'do not use partition'
                             }
        file_system = _file_system_type[fsType]
        combobox = self.select_single('GtkComboBox', BuilderName='partition_use_combo')
        combobox.select_filesystem_format(file_system)

    def set_mount_point(self, mntPoint=None):
        """ Sets the mount point for the partition """
        logger.debug("set_mount_point({0})".format(mntPoint))
        if mntPoint:
            combobox = self.select_single('GtkComboBox', BuilderName='partition_mount_combo')
            combobox.select_item(mntPoint, enter=False)

        return

    def check_dialog_objects(self, ):
        objects = ['partition_mount_combo', 'partition_use_combo',
                   'partition_create_type_primary', 'partition_create_type_logical',
                   'partition_create_place_beginning', 'partition_create_place_end',
                   ]
        for name in objects:
            obj = self.select_single(BuilderName=name)
            obj.check()
        expectThat(self.visible).equals(True, msg='Partition Dialog was not visible')

class GtkMessageDialog(GtkDialog):
    """ Emulator class for a GtkMessageDialog, """
    def __init__(self, *args):
        super(GtkMessageDialog, self).__init__(*args)
        self.pointing_device = Pointer(Mouse.create())
