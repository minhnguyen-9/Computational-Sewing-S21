
#include "triangle.h"
#include "plane.h"
#include <iostream>

#define Dot(x, y)	((x).dot((y)))
#define Cross(x,y)	((x).cross((y)))


bool PointInSegmentRange(const Vector3 & c, const Vector3 & a, const Vector3 & b, double &t, Vector3 &d, double rangeEps=1e-6)
{
	double len = (b - a).norm();
	Vector3 ab = (b - a)/len;
	// Project c onto ab, computing parameterized position d(t) = a + t*(b – a)
	t = (c - a).dot(ab) / ab.dot(ab);
	// If outside segment, clamp t (and therefore d) to the closest endpoint
	if (t > len+rangeEps) return 0;
	if (t < -rangeEps-.001) return 0;
	// Compute projected position from the clamped t
	d = a + t * ab;

	return 1;
}
/*
void ClosestPtPointSegment(Vector3 c, Vector3 a, Vector3 b, double &t, Vector3 &d)
{
	Vector3 ab = b - a;
	// Project c onto ab, computing parameterized position d(t) = a + t*(b – a)
	t = (c - a).dot(ab) / ab.dot(ab);
	// If outside segment, clamp t (and therefore d) to the closest endpoint
	if (t < 0.0f) t = 0.0f;
	if (t > 1.0f) t = 1.0f;
	// Compute projected position from the clamped t
	d = a + t * ab;
}*/

void Triangle::Transform(Transform3 & transform)
{

}

Vector3 Triangle::ComputeClosestPoint(const Vector3 & p) const
{
	const Vector3 & a = v[0];
	const Vector3 & b = v[1];
	const Vector3 & c = v[2];

	Vector3 ab = b - a;
	Vector3 ac = c - a;
	Vector3 ap = p - a;

	// Check if P in vertex region outside A
	double d1 = Dot(ab, ap);
	double d2 = Dot(ac, ap);
	if (d1 <= 0.f && d2 <= 0.f) {
		return a;
	}

	// Check if P in vertex region outside B
	Vector3 bp = p - b;
	double d3 = Dot(ab, bp);
	double d4 = Dot(ac, bp);
	if (d3 >= 0.f && d4 <= d3) {
		return b;
	}

	// Check if P in edge region of AB, if so return projection of P onto AB
	double vc = d1*d4 - d3*d2;
	if (vc <= 0.f && d1 >= 0.f && d3 <= 0.f) {
		double v = d1 / (d1 - d3);
		return a + v * ab;
	}

	// Check if P in vertex region outside C
	Vector3 cp = p - c;
	double d5 = Dot(ab, cp);
	double d6 = Dot(ac, cp);
	if (d6 >= 0.f && d5 <= d6) {
		return c;
	}

	// Check if P in edge region of AC, if so return projection of P onto AC
	double vb = d5*d2 - d1*d6;
	if (vb <= 0.f && d2 >= 0.f && d6 <= 0.f) {
		double w  = d2 / (d2 - d6);
		return a + w * ac;
	}

	// Check if P in edge region of BC, if so return projection  of P onto BC
	double va = d3*d6 - d5*d4;
	if (va <= 0.f && (d4 - d3) >= 0.f && (d5 - d6) >= 0.f)  {
		double w = (d4 - d3) / ((d4 - d3) + (d5 - d6));
		return b + w * (c - b);
	}

	// P inside face region. Compute X through its barycentric coordinates (u, v, w)
	double denom = 1.f / (va + vb + vc);
	double v = vb * denom;
	double w = vc * denom;
	return a + v * ab + w * ac;
}

double distance3DD(const double p0[3], const double p1[3])
{
	return sqrt( (p1[0]-p0[0])*(p1[0]-p0[0]) + (p1[1]-p0[1])*(p1[1]-p0[1]) + (p1[2]-p0[2])*(p1[2]-p0[2]) );
}

inline double TriArea2D(double x1, double y1, double x2, double y2, double x3, double y3)
{
	return (x1-x2)*(y2-y3) - (x2-x3)*(y1-y2);
}

bool TriSegIntersect(Triangle & tri, Vector3 & e1, Vector3 & e2, Vector3 & iPos, double & _t, Vector3 & norSq, double & u, double & v, double & w)
{
	Vector3 p = e1;
	Vector3 q = e2;
	const Vector3 & a = tri.v[0];
	const Vector3 & b = tri.v[1];
	const Vector3 & c = tri.v[2];

	Vector3 ab = b - a;
	Vector3 ac = c - a;
	Vector3 qp = p - q;
	// Compute triangle normal. Can be precalculated or cached if
	// intersecting multiple segments against the same triangle
	Vector3 n = Cross(ab, ac);
	// Compute denominator d. If d <= 0, segment is parallel to or points
	// away from triangle, so exit early
	float d = Dot(qp, n);
	if (d <= 0.0f) {
		qp = -qp;
		std::swap(p, q);
		d = -d;
	}

	Vector3 ap = p - a; 
	double t = Dot(ap, n);
	if (t < 0.0f) return 0;
	if (t > d) return 0; // For segment; exclude this code line for a ray test
	// Compute barycentric coordinate components and test if within bounds
	Vector3 e = Cross(qp, ap);
	v = Dot(ac, e);
	if (v < 0.0f || v > d) return 0;
	w = -Dot(ab, e);
	if (w < 0.0f || v + w > d) return 0;
	// Segment/ray intersects triangle. Perform delayed division and
	// compute the last barycentric coordinate component
	double ood = 1.0f / d;
	t *= ood;
	v *= ood;
	w *= ood;
	u = 1.0f - v - w;
	_t = t;
	iPos = u*a+v*b+w*c;
	norSq = n;
	return 1;//*/
}
/*
 bool TriRayIntersect(Triangle & tri, SRay & ray, SRayIntersectData & data)
 {
	 return TriRayIntersect(tri, ray.p, ray.d, data.pos, data.t, data.nor, data.u, data.v, data.w);
 }*/

void Triangle::ComputeBarycentricCoords(const Vector3 & pt, double * baryCoords) const
{
	const Vector3 & a = v[0];
	const Vector3 & b = v[1];
	const Vector3 & c = v[2];
	const Vector3 & p = pt;
	double & u = baryCoords[0];
	double & _v = baryCoords[1];
	double & w = baryCoords[2];

	Vector3 v0(b - a);
	Vector3 v1(c - a);
	Vector3 v2(p - a);
	float d00 = Dot(v0, v0);
	float d01 = Dot(v0, v1);
	float d11 = Dot(v1, v1);
	float d20 = Dot(v2, v0);

	float d21 = Dot(v2, v1);
	float denom = d00 * d11 - d01 * d01;
	_v = (d11 * d20 - d01 * d21) / denom;
	w = (d00 * d21 - d01 * d20) / denom;
	u = 1.0f - _v - w;
}

Vector3 Triangle::ComputePointFromBaryCoords(const double * baryCoords) const
{
	return v[0]*baryCoords[0] + v[1]*baryCoords[1] + v[2]*baryCoords[2];
}

bool Triangle::PointInTriangle(const Vector3 & pt, double * bary) const
{
	ComputeBarycentricCoords(pt, bary);
	return 
		0 <= bary[0] && bary[0] <= 1 &&
		0 <= bary[1] && bary[1] <= 1 &&
		0 <= bary[2] && bary[2] <= 1;
}

Vector3 Triangle::OffsetPointFromBorder(const Vector3 & _pt, double offsetScale) const
{
	Vector3 pt(_pt);
	const Vector3 offset = -Centroid();
	pt += offset;
	Triangle centeredTri(offsetScale*(v[0]+offset), offsetScale*(v[1]+offset), offsetScale*(v[2]+offset));
	pt = centeredTri.ComputeClosestPoint(pt);
	pt -= offset;

	return pt;
}

Vector3 Triangle::ProjectVector(const Vector3 & dir) const
{
	Vector3 n(Normal());
	double dot = dir.dot(n);
	return dir - dot*n;
}

void Triangle::ComputeIntersectedEdge(const Vector3 & rayPos, const Vector3 & rayDir, int & edgeIdx, Vector3 & intersection) const
{
	Vector3 triNor(Normal());
	Vector3 planeNor(rayDir.cross(triNor));
	Plane plane(rayPos, planeNor);
	
	int edgeIdxs[2];
	Vector3 intersections[2];
	plane.TriangleIntersection(*this, intersections, edgeIdxs);

	if (rayDir.dot(intersections[0] - intersections[1]) > 0) {
		edgeIdx = edgeIdxs[0];
		intersection = intersections[0];
	} else {
		edgeIdx = edgeIdxs[1];
		intersection = intersections[1];
	}
}

void Triangle::ComputeIntersectedEdges(const Vector3 & rayPos, const Vector3 & rayDir, int & edgeIdx, Vector3 & intersection) const
{
	Vector3 triNor(Normal());
	Vector3 planeNor(rayDir.cross(triNor));
	Plane plane(rayPos, planeNor);
	
	int edgeIdxs[2];
	Vector3 intersections[2];
	plane.TriangleIntersection(*this, intersections, edgeIdxs);

	if (rayDir.dot(intersections[0] - intersections[1]) < 0) {
		edgeIdx = edgeIdxs[0];
		intersection = intersections[0];
	} else {
		edgeIdx = edgeIdxs[1];
		intersection = intersections[1];
	}
}

bool Triangle::ComputeIntersection(const Vector3 & rayStart, const Vector3 & rayDir, Vector3 & intersection) const
{
	const Vector3 & p = rayStart;
	const Vector3 & a = v[0];
	const Vector3 & b = v[1];
	const Vector3 & c = v[2];

	Vector3 pq =  rayDir;
	Vector3 pa = a - p;
	Vector3 pb = b - p;
	Vector3 pc = c - p;

	Vector3 m = pq.cross(p);
	double u = pq.dot(c.cross(b)) + m.dot(c - b);
	if (u < 0.0f) return 0;
	double _v = pq.dot(a.cross(c)) + m.dot(a - c);
	if (_v < 0.0f) return 0;
	double w = pq.dot(b.cross(a)) + m.dot(b - a);
	if (w < 0.0f) return 0;

	double denom = 1.0f / (u + _v + w);
	u *= denom;
	_v *= denom;
	w *= denom; 

	intersection = u*v[0] + _v*v[1] + w*v[2];

	return 1;
}

/*
bool SplitTriangle(const Plane & plane, const Triangle & tri, Triangle * triOut, Vector3 * intersectionPts, const double lenEps)
{
	Segment e[3];
	e[0] = Segment(tri.v[0], tri.v[1]);
	e[1] = Segment(tri.v[1], tri.v[2]);
	e[2] = Segment(tri.v[2], tri.v[0]);

	int index = 0;
	if (!plane.TriangleIntersection(tri, intersectionPts, &index)) return 0;

	// First triangle:
	// c[index], c[(index+1)%3], tri.v[(index+1)%3]
	triOut[0].v[0] = intersectionPts[0];
	triOut[0].v[1] = intersectionPts[1];
	triOut[0].v[2] = tri.v[index];
	triOut[0].borderEdgeIndex[0] = -1;
	triOut[0].borderEdgeIndex[1] = tri.borderEdgeIndex[(index+2)%3];
	triOut[0].borderEdgeIndex[2] = tri.borderEdgeIndex[index];
	double d = triOut[0].SmallestLen();
	if (d < lenEps) __debugbreak();//return 0;

	// Second triangle:
	// c[(index+1)%3], tri.v[(index+2)%3], tri.v[(index+3)%3]
	triOut[1].v[0] = intersectionPts[0];
	triOut[1].v[1] = tri.v[(index+1)%3];
	triOut[1].v[2] = tri.v[(index+2)%3];
	triOut[1].borderEdgeIndex[0] = tri.borderEdgeIndex[index];
	triOut[1].borderEdgeIndex[1] = tri.borderEdgeIndex[(index+1)%3];
	triOut[1].borderEdgeIndex[2] = -1;
	d = triOut[1].SmallestLen();
	if (d < lenEps) __debugbreak();//return 0;

	// Third triangle:
	// tri.v[(index+3)%3], c[index], c[(index+1)%3]
	triOut[2].v[0] = tri.v[(index+2)%3];
	triOut[2].v[1] = intersectionPts[1];
	triOut[2].v[2] = intersectionPts[0];
	triOut[2].borderEdgeIndex[0] = tri.borderEdgeIndex[(index+2)%3];
	triOut[2].borderEdgeIndex[1] = -1;
	triOut[2].borderEdgeIndex[2] = -1;
	d = triOut[2].SmallestLen();
	if (d < lenEps) __debugbreak();//return 0;

	return 1;
}
*/

void Map2Dto3D(const Triangle & tri2D, const Vector3 & pt2D, const Triangle & tri3D, Vector3 & pt3D)
{
	double bary[3];
	tri2D.ComputeBarycentricCoords(pt2D, bary);
	pt3D = tri3D.ComputePointFromBaryCoords(bary);
}

void Map3Dto2D(const Triangle & tri3D, const Vector3 & pt3D, const Triangle & tri2D, Vector3 & pt2D)
{
	double bary[3];
	tri3D.ComputeBarycentricCoords(pt3D, bary);
	pt2D = tri2D.ComputePointFromBaryCoords(bary);
}
