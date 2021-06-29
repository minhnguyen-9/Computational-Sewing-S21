
#ifndef INCLUDE_H
#define INCLUDE_H

#define EIGEN_DONT_ALIGN_STATICALLY
#define EIGEN_DONT_VECTORIZE
#define EIGEN_DISABLE_UNALIGNED_ARRAY_ASSERT

#include <Eigen/Dense>
#include <Eigen/StdVector>
#include <Eigen/Geometry> 

#define USE_DOUBLE_PRECISION
#ifdef USE_DOUBLE_PRECISION
	typedef double RScalar;
	typedef Eigen::Vector2d Vector2;
	typedef Eigen::Vector3d Vector3;
	typedef Eigen::Matrix2d Matrix2;
	typedef Eigen::Matrix3d Matrix3;
	typedef Eigen::Matrix4d Matrix4;
	typedef Eigen::Quaternion<RScalar> Quaternion;
	typedef Eigen::Transform<RScalar, 2, Eigen::Affine> Transform2;
	typedef Eigen::Transform<RScalar, 3, Eigen::Affine> Transform3;
#else 
	typedef float RScalar;
	typedef Eigen::Vector2f Vector2;
	typedef Eigen::Vector3 Vector3;
	typedef Eigen::Vector4f Vector4;
	typedef Eigen::Matrix2f Matrix2;
	typedef Eigen::Matrix3f Matrix3;
	typedef Eigen::Matrix4f Matrix4;
	typedef Eigen::Quaternion<float> Quaternion;
	typedef Eigen::Transform<float, 2, Eigen::Affine> Transform2;
	typedef Eigen::Transform<float, 3, Eigen::Affine> Transform3;
#endif

#define NOMINMAX
#include <memory>
#include <string>

#define NOMINMAX
#include <Windows.h>
#include <memory>
#include <string>

#define CheckFinite(_vec)												\
{																		\
	if (!isfinite((_vec).x())) {										\
		std::cout << __FILE__ << ' ' << __LINE__ << ' ' << std::endl;	\
		__debugbreak();	}												\
}

inline int mod(int a, int b)
{
	return (a%b + b) % b;
}

template <typename T>
inline T Clamp(T val, T a, T b)
{
	if (val < a) val = a;
	if (val > b) val = b;
	return val;
}

#define Dot(x, y)	((x).dot((y)))
#define Cross(x,y)	((x).cross((y)))

struct Segment {
	Vector3 e1;
	Vector3 e2;
public:
	Segment()  {}
	Segment(const Vector3 & _e1, const Vector3 & _e2):e1(_e1), e2(_e2) {; }

	double SegDist() const {return (e2-e1).norm(); }
	Vector3 Interpolate(double t) const {return  (1.0-t)*e1 + t*e2; }
	Vector3 Midpoint() const {return .5*e1 + .5*e2; }
};

#endif