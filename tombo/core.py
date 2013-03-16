'''
Created on Feb 19, 2012

@author: Michael P
'''
import yaml
import logging
import os
from tombotreemodel import FolderNode
from tombotreemodel import SimpleNoteNode
from tombotreemodel import TreeViewModel
from tombo_codec import TomboCodec


class Core():
    '''
    Core class for Tombo
    Handles
        Logging
        TreeModel Operations
        Config loads, edition, saving
    '''

    def load_config(self):
        stream = open(self.config_file_name, 'r')
        self.config = yaml.load(stream)

    def save_config(self):
        stream = open(self.config_file_name, 'w')
        yaml.dump(self.config, stream, default_flow_style=False)

    def restore_default_config(self):
        default_config_dictionary = {
                            'root': "C:\\tombo_reinc_test_root_folder",
                            'memo': {
                                 'root': "",
                                 'sync file name and title': True,
                                 'open notes read only mode': False
                                 },
                            'toppage': {
                                     'open item last selected': False,
                                     'default note': "tombo://default/"
                                     },
                            'security': {
                                      'password timeout': 5,
                                      'use random filename': False
                                      },
                            'font': {
                                  # TODO: Tahoma 9 cleartype?
                                  'tree': {'default': True, 'Font': ''},
                                  'memo': {'default': True, 'Font': ''}
                                  },
                            'date': {
                                  'date1': '%y/%M/%d',
                                  'date2': '%h:%m:%s'
                                  },
                            'memoview': {
                                      'keep cursor position': False,
                                      'tabstop': 8,
                                      'showtitle': True,
                                      'disable save dialog': False
                                      },
                            'externalapps': {
                                          'application1': '',
                                          'application2': ''
                                          },
                            'encoding': {
                                      'current encoding': 'system native',
                                      'possible encodings': ['utf8', 'cp1251']
                                      },
                            'color': {
                                   'foreground': '',
                                   'background': '',
                                   'endofline': '',
                                   'enoflinefolding': '',
                                   'tab': '',
                                   'eof': ''
                                   },
                    }
        # TODO: ask for root folder
        self.config = default_config_dictionary
        self.save_config()

    def __init__(self):
        """ Initialize core """
        #init logger
        self.config_file_name = "config.yaml"
        self.log_name = "tombo.log"

        self.logger = self.init_logger()

        self.logger.info("reading config file: %s",
                         os.path.join(os.curdir, self.config_file_name))

        self.load_config()

        self.logger.info("root folder set to: %s", self.config['root'])

        self.model = self.createTreeModel()
        self.logger.info("TreeModel initialized")

        self.codec = TomboCodec(self.config['encoding']['possible encodings'])

    def init_logger(self, path=os.path.curdir):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        logfile_name = os.path.join(path, self.log_name)
        formatter = logging.Formatter(
            '%(asctime)s [%(levelname)s] %(name)s - %(message)s',
            datefmt="%Y-%m-%d %H:%M:%S"
            )

        fileHandler = logging.FileHandler(filename=logfile_name)
        fileHandler.setLevel(logging.INFO)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(logging.INFO)
        streamHandler.setFormatter(formatter)
        logger.addHandler(streamHandler)

        return logger

    def scan_folder_for_notes_recursive(self, path, parent_node):
        self.logger.info("Scanning folder: %s", path)

        dirs = [name for name in os.listdir(path) if os.path.isdir(
                                            os.path.join(path, name))]
        files = [name for name in os.listdir(path) if os.path.isfile(
                                            os.path.join(path, name))]

        for file in files:
            #TODO: skip the not .txt and .chi files
            #TODO: remove "txt", "chi" from node name
            SimpleNoteNode(file, file, parent_node)

        for dirname in dirs:
            self.logger.info("Folder found: %s", dirname)
            folder_node = FolderNode(dirname, parent_node)
            self.scan_folder_for_notes_recursive(
                    os.path.join(path, dirname), folder_node)

    #TODO: implement add_parent_path_recursive
    def add_parent_path_recursive(self, node):

        if node.parent() == None:
            return self.config['root']
        else:
            path = self.add_parent_path_recursive(node.parent())
            return os.path.join(path, node.name())

#            if node is FolderNode:
#                currentFolder = FolderNode(node).name()
#                return os.path.join(path, currentFolder)
#            else: # TODO: Add check for encoded note
#                return os.path.join(path, SimpleNoteNode(node).filename)

    def createTreeModel(self):
        self.logger.info("Creating TreeModel")
        root_node = FolderNode("TestRootNode")
        self.logger.info("Scanning system for notes")
        self.scan_folder_for_notes_recursive(self.config["root"], root_node)
        return TreeViewModel(root_node)

    def get_note_text(self, path_to_file):

        # define file type
        base_name = os.path.basename(path_to_file)
        # TODO: use note_name
        # note_name, file_extension = os.path.splitext(base_name)
        file_extension = os.path.splitext(base_name)

        # get file content in bytes
        bytes_read = open(path_to_file, "rb").read()

        # if encripted - ask for password and decript.
        # if wrong password - show message
        if file_extension is "chi":
            bytes_read = self.codec.decode_chi_bytes(bytes_read)

        # decode to string
        encoding = self.codec.autodefine_encoding(path_to_file)

        string = bytes_read.decode(encoding)
        return string
