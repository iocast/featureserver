import math

class Simplify(object):
    def __call__(self, features, tolerance=0.001, maxvertices=None):
        tolerance = float(tolerance)
        if not maxvertices is None: maxvertices = int(maxvertices)
        vertices=0
        for i, feature in enumerate(features):
            if feature['geometry']['type'] == "Point": 
                vertices += 1
                continue
            if feature['geometry']['type'] == "LineString":
                line = feature['geometry']['coordinates']
                new_line = simplify_points(line, tolerance)
                vertices += len(new_line)
                feature['geometry']['coordinates'] = new_line
            elif feature['geometry']['type'] == "Polygon":
                line = feature['geometry']['coordinates'][0]
                new_line = simplify_points(line, tolerance)
                vertices += len(new_line)
                feature['geometry']['coordinates'][0] = new_line
            feature.properties['processed_by'] = "Simplify (tolerance=%s, maxvertices=%s)" % (tolerance, maxvertices)
            if not maxvertices is None and vertices > maxvertices: 
                return features[:i + 1]
        return features 

# ported from
#   http://www.3dsoftware.com/Cartography/Programming/PolyLineReduction/
#   By Schuyler Erle
   
def simplify_points (pts, tolerance): 
    """
    >>> line = [[0,0],[1,0],[2,0],[2,1],[2,2],[1,2],[0,2],[0,1],[0,0]]
    >>> simplify_points(line, 1.0)
    [[0, 0], [2, 0], [2, 2], [0, 2], [0, 0]]
    
    >>> line = [[0,0],[0.5,0.5],[1,0],[1.25,-0.25],[1.5,.5]]
    >>> simplify_points(line, 0.25)
    [[0, 0], [0.5, 0.5], [1.25, -0.25], [1.5, 0.5]]
    
    """
    anchor  = 0
    floater = len(pts) - 1
    stack   = []
    keep    = set()

    stack.append((anchor, floater))  
    while stack:
        anchor, floater = stack.pop()
      
        # initialize line segment
        if pts[floater] != pts[anchor]:
            anchorX = float(pts[floater][0] - pts[anchor][0])
            anchorY = float(pts[floater][1] - pts[anchor][1])
            seg_len = math.sqrt(anchorX ** 2 + anchorY ** 2)
            # get the unit vector
            anchorX /= seg_len
            anchorY /= seg_len
        else:
            anchorX = anchorY = seg_len = 0.0
    
        # inner loop:
        max_dist = 0.0
        farthest = anchor + 1
        for i in range(anchor + 1, floater):
            dist_to_seg = 0.0
            # compare to anchor
            vecX = float(pts[i][0] - pts[anchor][0])
            vecY = float(pts[i][1] - pts[anchor][1])
            seg_len = math.sqrt( vecX ** 2 + vecY ** 2 )
            # dot product:
            proj = vecX * anchorX + vecY * anchorY
            if proj < 0.0:
                dist_to_seg = seg_len
            else: 
                # compare to floater
                vecX = float(pts[i][0] - pts[floater][0])
                vecY = float(pts[i][1] - pts[floater][1])
                seg_len = math.sqrt( vecX ** 2 + vecY ** 2 )
                # dot product:
                proj = vecX * (-anchorX) + vecY * (-anchorY)
                if proj < 0.0:
                    dist_to_seg = seg_len
                else:  # calculate perpendicular distance to line (pythagorean theorem):
                    dist_to_seg = math.sqrt(abs(seg_len ** 2 - proj ** 2))
                if max_dist < dist_to_seg:
                    max_dist = dist_to_seg
                    farthest = i

        if max_dist <= tolerance: # use line segment
            keep.add(anchor)
            keep.add(floater)
        else:
            stack.append([anchor, farthest])
            stack.append([farthest, floater])

    keep = list(keep)
    keep.sort()
    return [pts[i] for i in keep]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
