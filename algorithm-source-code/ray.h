
#ifndef RAY_H
#define RAY_H

#include "include.h"

struct SRay {
	Vector3 d;
	Vector3 p;
public:
	SRay() {}
	//~SRay() {}

	/* The transformation must strictly be a rotation and translation */
	/*void Transform(Matrix4x4F & rT) {
		p = rT*p;
		d = rT^d;
	}*/
};

struct SRayIntersectData {
	Vector3 pos;
	Vector3 nor;
	int iBody;
	int iTri;
	double t;
	
	/* Barycentric coordinates */
	double u, v, w;
};

#endif