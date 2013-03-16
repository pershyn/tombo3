'''
Created on Apr 10, 2012

@author: Mykhailo.Pershyn
'''
import os
import shutil


class TomboCripter():
    """
        Performs encription and decription to *.chi tombo encoded format
    """

    def __init__(self):
        pass

    def decode_chi_bytes(self):
        # ask for password
        # try to decode file
        # return decoded sequence
        raise NotImplementedError()
        pass

    def encode_chi_file(self):
        # try to get stored password (used to encode the file)
        # if not found or outdated - ask for password
        # try to encode file
        # return encoded sequence
        raise NotImplementedError()
        pass


class TomboCodec():
    """
        - handles decoding and encoding of text files (uft8, cp1251, etc)
        - perform encoding auto-detection
        - performs conversion to utf8
    """

    def __init__(self, encodings):
        self.encodings = encodings
        pass

    def autodefine_encoding(self, filename):
        # gather the encodings you think that the file may be
        # encoded inside a tuple

        encodings = set(['utf8', 'cp1251'])
        print(encodings)

        # try to open the file and exit if some IOError occurs
        try:
            file_bytes = open(filename, 'rb').read()
        except Exception:
            print("file encoding failed to read file")
            pass

        # now start iterating in our encodings tuple and try to
        # decode the file

        for enc in encodings:
            try:
            # try to decode the file with the first encoding
            # from the tuple.
            # if it succeeds then it will reach break, so we
            # will be out of the loop (something we want on
            # success).
            # the string variable will hold our decoded text
                file_bytes.decode(enc)
                print("autodecode defined encoding {0}".format(enc))
                return enc

            except Exception as inst:
                # if the first encoding fail, then with the continue
                # keyword will start again with the second encoding
                # from the tuple an so on.... until it succeeds.
                # if for some reason it reaches the last encoding of
                # our tuple without success, then exit the program.
                print ("not succeeded with encoding {0}".format(enc))
                print(type(inst))
                print(inst.args)
                print(inst)
                continue
        print("Not succeeded with encodings")
        pass

    def convert_to_utf8(self, filename):
        # gather the encodings you think that the file may be
        # encoded inside a tuple
        encodings = ('windows-1253', 'iso-8859-7', 'macgreek', 'cp1251')

        # try to open the file and exit if some IOError occurs
        try:
            f = open(filename, 'r').read()
        except Exception:
            print("file encoding failed")
            pass

        # now start iterating in our encodings tuple and try to
        # decode the file

        for enc in encodings:
            try:
            # try to decode the file with the first encoding
            # from the tuple.
            # if it succeeds then it will reach break, so we
            # will be out of the loop (something we want on
            # success).
            # the data variable will hold our decoded text
                data = f.decode(enc)
                break

            except Exception:
                # if the first encoding fail, then with the continue
                # keyword will start again with the second encoding
                # from the tuple an so on.... until it succeeds.
                # if for some reason it reaches the last encoding of
                # our tuple without success, then exit the program.
                if enc == encodings[-1]:
                    print ("not succeeded with encoding")
                    break
                continue

        # now get the absolute path of our filename and append .bak
        # to the end of it (for our backup file)
        fpath = os.path.abspath(filename)
        newfilename = fpath + '.bak'

        # and make our backup file with shutil
        shutil.copy(filename, newfilename)
        # and at last convert it to utf-8
        f = open(filename, 'w')
        try:
            f.write(data.encode('utf-8'))
#        except Exception e:

        finally:
            f.close()
