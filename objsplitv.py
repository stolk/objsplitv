#!/usr/bin/python

import sys


def process_group( groupname, lines, vusage, verts, norms, newverts ) :
	print "Processing group", groupname
	for s in range( len( lines ) ) :
		if ( len( lines[s] ) > 2 and lines[s][2:] == groupname ) :
			break
	e = len(lines)
	for e in range( s+1, len(lines) ) :
		if ( lines[e][:2] == "g " ) :
			break

	glines = lines[s:e+1]

	gline  = [ x for x in glines if x[:2] == "g " ][ 0 ]

	mline  = [ x for x in glines if x[:7] == "usemtl " ][ 0 ]

	flines = [ x[2:] for x in glines if x[:2] == "f " ]
	print "num faces in group:", len(flines)

	newflines = []

	vertsadded = 0
	for fline in flines :
		idxlst = fline.split( ' ' )
		for i,idx in enumerate( idxlst ) :
			indices = idx.split('/')
			vidx = int( indices[ 0 ] )
			tidx = indices[ 1 ]
			nidx = int( indices[ 2 ] )
			nrm  = norms[ nidx-1 ]
			usage = str(nrm)+"-"+groupname

			usagemap = vusage[ vidx ]
			if len( usagemap ) == 0 :
				# first usage.
				usagemap[ usage ] = vidx
			elif usage in usagemap :
				newvidx = usagemap[ usage ]
				newidx = "%d/%s/%d" % ( newvidx, tidx, nidx )
				if newvidx != vidx :
					#print "Re-using split-off vertex idx", newvidx, "to replace", vidx
					idxlst[ i ] = newidx
			else :
				# we are not the only user.
				newvidx = len(verts) + len(newverts) + 1
				usagemap[ usage ] = newvidx
				newidx = "%d/%s/%d" % ( newvidx, tidx, nidx )
				#print "splitting off from vertex idx", vidx, "as new vertex index", newvidx
				idxlst[ i ] = newidx
				newverts.append( verts[ vidx-1 ] )
				vertsadded += 1
		newfline = ""
		for idx in idxlst :
			newfline += ( idx+" " )
		newflines.append( "f " + newfline )

	newvlines = []
	for v in newverts[-vertsadded:] :
		newvlines.append( "v " + v )

	return [ gline, mline ] + newvlines + newflines


def process_object( objname, lines ) :
	print "Processing object", objname
	for s in range( len( lines ) ) :
		if ( len( lines[s] ) > 2 and lines[s][2:] == objname ) :
			break
	e = len(lines)
	for e in range( s+1, len( lines ) ) :
		if ( lines[e][:2] == "o " ) :
			break
	objlines = lines[s:e+1]

	verts = [ x[2:] for x in objlines if x[:2] == "v " ]
	norms = [ x[3:] for x in objlines if x[:3] == "vn " ]
	vcnt = len( verts )
	ncnt = len( norms )
	print "vertex count", vcnt, "normal count", ncnt

	vusage = [ {} for v in verts ]
	vusage.append( {} )

	newverts = []

	groupnames = [ x[2:] for x in objlines if x[:2] == "g " ]
	print "groups", groupnames

	newlines = [ lines[s] ]
	for v in verts :
		newlines.append( "v " + v )
	for n in norms :
		newlines.append( "vn " + n )
	for groupname in groupnames :
		newgrouplines = process_group( groupname, objlines, vusage, verts, norms, newverts )
		newlines += newgrouplines

	return newlines


def process_file( iname ) :
	oname = iname.replace( ".obj", "-split.obj" )
	try :
		f = open( iname, "r" )
		lines = f.readlines()
		lines = [ x.strip() for x in lines ]
		f.close()
	except:
		print "Cannot open '%s' for reading." % ( iname, )
		return False

	objnames = [ x[2: ] for x in lines if x[:2] == "o " ]

	lineidx = lines.index( "o " + objnames[ 0 ] )

	try:
		f = open( oname, "w" )
	except:
		print "Cannot open '%s' for writing." % ( oname, )
		return False

	for i in range( lineidx ) :
		f.write( lines[ i ] + "\n" )

	for objname in objnames :
		newlines = process_object( objname, lines )
		for line in newlines :
			f.write( line + "\n" )


if len( sys.argv ) < 2 :
	print "Usage: %s input.obj" % ( sys.argv[0], )

ifiles = sys.argv[1:]
for ifile in ifiles :
	process_file( ifile )

