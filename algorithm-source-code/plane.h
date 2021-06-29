
#ifndef PLANE_H
#define PLANE_H

#include "triangle.h"

class Plane  {
public:
	Vector3 point;
	Vector3 n;
public:
	Plane() {}
	Plane(const Plane & copy) {memcpy(this, &copy, sizeof(Plane));}
	Plane(const Vector3 & _pt, const Vector3 & _n):point(_pt), n(_n) {
		n.normalize();
	}
	Plane(const Vector3 & p1, const Vector3 & p2, const Vector3 & p3) {
		Vector3 v1(p2 - p1);
		Vector3 v2(p3 - p1);
		n = Vector3(v1.cross(v2)).normalized();
		point = p1;
	}

	void ComptuePlane(std::vector<Vector3> & curve);

	bool PointUnderPlane(const Vector3 & pt, double & dist) const;
	/*double DistanceToPlane(const Vector3 & pt);
	//The plane must be normalized
	Vector3 ClosestPointOnPlane(const Vector3 & pt);*/

	bool TriangleIntersection(const Triangle & tri) const;
	// Compute the points of intersection if the triangle intersects
	bool TriangleIntersection(const Triangle & tri, Vector3 * intersectionPts, int * intersectionEdgeIndices=NULL) const;

	bool SegmentIntersection(const Vector3 & start, const Vector3 & end, Vector3 & intersectionPt) const;

	Plane & operator=(const Plane & pl) {
		n = pl.n;
		point = pl.point;

		return *this;
	}
};


inline bool Plane::PointUnderPlane(const Vector3 & pt, double & dist) const
{
	Vector3 v(pt - point);
	dist = v.dot(n);
	return dist < 0;
}

/* Compute signed distance to plane. 
inline double Plane::DistanceToPlane(const Vector3 & pt)
{
	return Com::Dot(pt, n) - d;
}

//The plane must be normalized
inline Vector3 Plane::ClosestPointOnPlane(const Vector3 & pt)
{
	double dist = Com::Dot(pt, n);
	Vector3 c((dist-d)*n);
	return pt - c;
}*/


inline void Compute2DPlaneBasis(const Plane & pl, Vector3 & v1, Vector3 & v2)
{
	Vector3 up(0.0, 1.0, 0.0);
	v1 = up.cross(pl.n);
	if (v1.norm() < 1e-4) v1 = Vector3(0, 0, 1.f);
	v2 = pl.n.cross(v1);
}

/*
inline Vector2F ProjectPointTo2DPlaneBasis(Vector3 & pt, Vector3 & o, Vector3 & v1, Vector3 & v2)
{
	Vector3 p(pt - o);
	return Vector2F(DotXYZ(v1, p), DotXYZ(v2, p));
}*/


#endif