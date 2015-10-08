#objsplitv

##Introduction

The Wavefront OBJ file format for 3D models, allows faces to share a vertex positions, and at the same time use a different vertex normal for that shared coordinate.
From here on, I will refer to this as 'inappropriate vertex sharing.'

This sharing will cause problems in some scenarios.
One of these is when you want to bake a lighting solution (from radiosity, photonmapper, or an ambient occlusion algorithm e.g.) onto the vertices.
The lighting on the faces will differ a lot, due to the different surface normals, so multiple colours will need to be assigned to this single vertex!
Hence, these inappropriately shared vertices need to be split.

Note that Wavefront OBJ also alows sharing vertex positions over different materials. 
Again, this causes problems when trying to bake to the vertex colours.

##Cases

An example case of where inappropriately shared vertices are generated, is in the Wavefront OBJ exporter of the excellent [Wings3D](http://www.wings3d.com) modeling tool.
You can run objsplitv on the output from Wings3D to clean up this issue.
In the example below, vertex A can be safely shared, due to the identical normal for incident faces.
But vertex B has three different face normals, and should not be shared for the purpose of baking light.

![Sample](doc/sharing.png "Sample of appropriate (A) and inappropriate (B) sharing of vertex coordinates.")

##Dependencies

objsplitv requires Python.

##Example Use

$ ./objsplitv.py input.obj

This will generate a split-input.obj file.

## Bugs

No known bugs.

## Thanks

* Thank you Wings3D team, for making a most excellent modeling tool.

## License

Copyright 2012 [Abraham T. Stolk](http://stolk.org)

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

   [http://www.apache.org/licenses/LICENSE-2.0](http://www.apache.org/licenses/LICENSE-2.0)

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
