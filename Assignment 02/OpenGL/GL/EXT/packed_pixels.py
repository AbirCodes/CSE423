'''OpenGL extension EXT.packed_pixels

This module customises the behaviour of the 
OpenGL.raw.GL.EXT.packed_pixels to provide a more 
Python-friendly API

Overview (from the spec)
	
	This extension provides support for packed pixels in host memory.  A
	packed pixel is represented entirely by one unsigned byte, one
	unsigned short, or one unsigned integer.  The fields with the packed
	pixel are not proper machine types, but the pixel as a whole is.  Thus
	the pixel storage modes, including PACK_SKIP_PIXELS, PACK_ROW_LENGTH,
	PACK_SKIP_ROWS, PACK_IMAGE_HEIGHT_EXT, PACK_SKIP_IMAGES_EXT,
	PACK_SWAP_BYTES, PACK_ALIGNMENT, and their unpacking counterparts all
	work correctly with packed pixels.

The official definition of this extension is available here:
http://www.opengl.org/registry/specs/EXT/packed_pixels.txt
'''
from OpenGL import platform, constant, arrays
from OpenGL import extensions, wrapper
import ctypes
from OpenGL.raw.GL import _types, _glgets
from OpenGL.raw.GL.EXT.packed_pixels import *
from OpenGL.raw.GL.EXT.packed_pixels import _EXTENSION_NAME

def glInitPackedPixelsEXT():
    '''Return boolean indicating whether this extension is available'''
    from OpenGL import extensions
    return extensions.hasGLExtension( _EXTENSION_NAME )


### END AUTOGENERATED SECTION