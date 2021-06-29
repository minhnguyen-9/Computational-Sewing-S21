
#include "plane.h"

void Plane::ComptuePlane(std::vector<Vector3> & curve)
{
	Vector3 u, v;
	n = Vector3(0, 0, 0);
	point = Vector3(0, 0, 0);
	const int X=0,Y=1,Z=2;
	for (int i=0, end=curve.size(); i<end; i++) {
        u = curve[i];
        v = curve[(i + 1) % end];
        n[X] += (u[Y] - v[Y]) * (u[Z] + v[Z]);
        n[Y] += (u[Z] - v[Z]) * (u[X] + v[X]);
        n[Z] += (u[X] - v[X]) * (u[Y] + v[Y]);
		point += u;
	}
	n.normalize();
	point /= curve.size();
}

bool Plane::TriangleIntersection(const Triangle & tri) const
{
	double dist;
	int sum = PointUnderPlane(tri.v[0], dist) + PointUnderPlane(tri.v[1], dist) + PointUnderPlane(tri.v[2], dist);
	return sum != 3 && sum != 0;
}

bool Plane::TriangleIntersection(const Triangle & tri, Vector3 * intersectionPts, int * intersectionEdgeIndices) const
{
	if (!TriangleIntersection(tri)) return false;
	
	double dist;
	bool b[3] = {PointUnderPlane(tri.v[0], dist), PointUnderPlane(tri.v[1], dist), PointUnderPlane(tri.v[2], dist)};
	
	int index = 0;
	int sum = b[0]+b[1]+b[2];
	if (sum == 1) while (b[index] != 1) index++;
	else while (b[index] != 0) index++;
	assert(index < 3);

	SegmentIntersection(tri.v[index], tri.v[(index+1)%3], intersectionPts[0]);
	SegmentIntersection(tri.v[(index+2)%3], tri.v[index], intersectionPts[1]);

	if (intersectionEdgeIndices) {
		intersectionEdgeIndices[0] = index;
		intersectionEdgeIndices[1] = mod(index+2,3);
	}

	return true;
}

bool Plane::SegmentIntersection(const Vector3 & start, const Vector3 & end, Vector3 & intersectionPt) const
{
	Vector3 dir(end-start);
	
	double d = point.dot(n);
	double t = (d - n.dot(start))/n.dot(dir);

	if (t >= 0 && t <= 1) {
		intersectionPt = start + t * dir;
		return true;
	}

	return false;
}
