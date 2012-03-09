import struct
import logging

class CStruct(object):
    def __init__(self, definition):
        self.__definition = definition

    def __str__(self):
        result = str()

        for name, form in self.__definition:
            try:
                value = getattr(self, name)

                if isinstance(value, tuple):
                    for index, f in enumerate(value):
                        result += "{0}[{1}] = \n{2}".format(name, index,
                                                          add_tab(str(f)))
                else:
                    result += "{0} = {1}\n".format(name, value)
            except AttributeError:
                result += "{0} = {1}\n".format(name, None)

        return(result)
        
    def from_stream(self, data):
        stream_to_tuple(data, self.__definition, self)        

def add_tab(string, tabs=1):
    result = str()
    for line in string.split("\n"):
        result += "\t{0}\n".format(line)

    return(result)

def stream_to_tuple(data, structure_definition, target):
    """Given the structure of interest, populates the named tuple with the
appropriate data. Ideally, this could be done with tuple._make(struct.unpack())),
but strings do not seem to work properly in this case."""
    for index, definition in enumerate(structure_definition):
        name, form = definition
        number, formtype = form
        logging.debug("{0}: {1}".format(name, form))

        if type(formtype) == type(str()):
            # We have a string format, so no recursion
            formstr = "{0}{1}".format(number, formtype)
            logging.debug("Reading {0} from stream.".format(formstr))
            value = struct.unpack_from(formstr,
                                    data.read(
                                        struct.calcsize(formstr)).encode())            

            # Now that we have the data, we need to consider whether it is an
            # array or a single value. If a character array, create a string.
            # If a numerical array, make a list. If a single value, make a
            # single value
            if form[-1] in "?hHiIlLqQfdP":
                # Numerical value
                if len(form) == 1:
                    # Single value
                    value = value[0]
                else:
                    value = list(value[:-1])
            else:
                # Character value
                # Kludge to get rid of "\x00". This should be possible using nicer
                # methods.
                value = bytes("".encode()).join(value).decode()
                
            setattr(target, name, value)
        else:
            # Recursion!
            logging.debug("Recursing!")
            setattr(target, name, tuple([CStruct(formtype) for i in range(number)]))
            for i in range(number):
                stream_to_tuple(data, formtype, getattr(target, name)[i])

if __name__ == "__main__":
##    logging.basicConfig(level=logging.DEBUG)
    blargh_t = [
        ("blargh", (4, "i")),
        ("cool", (4, "c"))]

    nyargh_t = [
        ("nyargh", (2, "c")),
        ("fjord", (2, blargh_t))]


    a = CStruct(nyargh_t)

    with open("WINHEAD.TXT") as data:
        a.from_stream(data)

    print(a)
