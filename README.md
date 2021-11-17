# JumpFloodingAlgorythm [wip]
A python numpy implementation of the jump flooding algorithm for calculating distance fields and Voronoi diagrams. 

Jump flooding algorithm is a fast, approximated, low error algorithm for computing rasterized voronoi diagrams and signed or unsigned distance fields. Image metrics are customizable, allowing to make periodic/tilable diagrams, or to compute accurate diagrams from Earth maps, taking the projection stretching into account (see SphericalMetric).

## Keyword features
- Voronoi diagram
- Distance field
- Signed distance field from image
- Euclidian and spherical metric
- (Signed) distancce maps: distance to coast, distance to cities
