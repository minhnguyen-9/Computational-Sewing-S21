
#ifndef TRIANGLE_H
#define TRIANGLE_H

#include "include.h"
#include "ray.h"
#include <vector>
#include <fstream>

class Plane;

struct Triangle {
	Triangle() {}
	Triangle(const Vector3 & v0, const Vector3 & v1, const Vector3 & v2) {
		v[0] = v0;
		v[1] = v1;
		v[2] = v2;
	}

	Vector3 v[3];

	Vector3 Normal() const {
		Vector3 v0(v[1]-v[0]);
		Vector3 v1(v[2]-v[0]);
		return v0.cross(v1).normalized();
	}

	void Transform(Transform3 & transform);
	Vector3 ComputeClosestPoint(const Vector3 & pt) const;
	void ComputeBarycentricCoords(const Vector3 & pt, double * baryCoords) const;
	Vector3 ComputePointFromBaryCoords(const double * baryCoords) const;
	bool PointInTriangle(const Vector3 & pt, double * baryCoords) const;
	Vector3 OffsetPointFromBorder(const Vector3 & pt, double offsetScale=.95) const;
	Vector3 ProjectVector(const Vector3 & dir) const;
	void ComputeIntersectedEdge(const Vector3 & rayPos, const Vector3 & rayDir, int & edgeIdx, Vector3 & intersection) const;
	void ComputeIntersectedEdges(const Vector3 & rayPos, const Vector3 & rayDir, int & edgeIdx, Vector3 & intersection) const;
	bool ComputeIntersection(const Vector3 & rayStart, const Vector3 & rayDir, Vector3 & intersection) const;

	Vector3 Centroid() const {
		return (v[0]+v[1]+v[2])/3.;
	}
	double Area() const {
		Vector3 e0(v[1]-v[0]);
		Vector3 e1(v[2]-v[0]);
		return e0.cross(e1).norm();
	}
	double SmallestEdgeLen() const {
		double l1 = (v[0]-v[1]).norm();
		double l2 = (v[1]-v[2]).norm();
		double l3 = (v[2]-v[0]).norm();
		l1 = l1 < l2 ? l1 : l2;
		return l1 < l3 ? l1 : l3;
	}
	double LargestEdgeLen() const {
		double l1 = (v[0]-v[1]).norm();
		double l2 = (v[1]-v[2]).norm();
		double l3 = (v[2]-v[0]).norm();
		l1 = l1 > l2 ? l1 : l2;
		return l1 > l3 ? l1 : l3;
	}
};

void Map2Dto3D(const Triangle & tri2D, const Vector3 & pt2D, const Triangle & tri3D, Vector3 & pt3D);
void Map3Dto2D(const Triangle & tri3D, const Vector3 & pt3D, const Triangle & tri2D, Vector3 & pt2D);

bool TriSegIntersect(Triangle & tri, Vector3 & e1, Vector3 & e2, Vector3 & iPos, double & t, Vector3 & norSq, double & u, double & v, double & w);
//bool TriRayIntersect(Triangle & tri, SRay & ray, SRayIntersectData & data);
//bool SplitTriangle(const Plane & plane, const Triangle & tri, Triangle * triOut, Vector3 * intersectionPts, const double lenEps=1e-3);


#endif