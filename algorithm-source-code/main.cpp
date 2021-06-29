
#include <iostream>

#include "triangle_mesh.h"

void RunProcess(const char * dir, char * cmdLine)
{
	STARTUPINFOA si;
	PROCESS_INFORMATION pi;

	ZeroMemory( &si, sizeof(si) );
	si.cb = sizeof(si);
	ZeroMemory( &pi, sizeof(pi) );
	
	if(!CreateProcessA("C:\\windows\\system32\\cmd.exe", cmdLine, NULL, NULL, NULL, FALSE, 0,
		dir, &si, &pi)) { __debugbreak(); }
	WaitForSingleObject( pi.hProcess, INFINITE );
}

void ComputeTrianlgeMatrix(const Triangle & _tri, Matrix3 & mat) 
{
	Triangle tri = _tri;
	Vector3 vec1 = tri.v[1]-tri.v[0];
	Vector3 vec2 = tri.v[2]-tri.v[0];
	double angle = acos(vec2.normalized().dot(vec1.normalized()));
	tri.v[0] = Vector3(0,0,0);
	tri.v[1] = vec1.norm() * Vector3(1, 0, 0);
	tri.v[2] = vec2.norm() * Vector3(cos(angle), sin(angle), 0);

	Vector3 v1 = tri.v[0];
	Vector3 v2 = tri.v[1];
	Vector3 v3 = tri.v[2];
	Vector3 v4 = 1e-2 * tri.Normal();
	//if (abs(1-v4.z()) > 1e-3) __debugbreak();	

	Vector3 c1(v2-v1);
	Vector3 c2(v3-v1);
	Vector3 c3(v4-v1);

	mat << c1.x(), c2.x(),  c3.x(),
			c1.y(), c2.y(),  c3.y(),
			c1.z(), c2.z(),  c3.z();
}

void ComputeQuaternion(const Vector3 & v1, const Vector3 & v2, Quaternion & q) 
{
	Vector3 v(v1.cross(v2));
	RScalar n = v.norm();
	if (n < 1e-4) {q = Quaternion::Identity(); return; }
	RScalar angle = acos(Clamp(v1.dot(v2), (RScalar)-1, (RScalar)1));
	q = Eigen::AngleAxis<RScalar>(angle, v/n);
	if (q.vec().dot(v) < 0) q = Quaternion(-q.w(), -q.x(), -q.y(), -q.z()); 
}

int main(int argc, char ** argv)
{
	char cmdLine[512], buf[512];
	const char * meshName = "cate";
	
	// Load target mesh
	TriangleMesh targetGarment; 
	sprintf(buf, "meshes/%s.obj", meshName);
	targetGarment.Create(buf);

	// Perform pattern correction to compute outputGarment
	TriangleMesh outputGarment = targetGarment;
	TriangleMesh simGarment;
	for (unsigned iter=0; iter<10; iter++) {
		std::cout << "iter " << iter << std::endl;

		// Compute initial parameterization using 3d panels
		if (iter == 0 && 1) {
			outputGarment.SavePanels("arap_l2\\input", 1);
			sprintf(cmdLine, "/C start matlab -nosplash -nodesktop -minimize -r RunAll -logfile matlab_log.txt");
			RunProcess("arap_l2", cmdLine);
			Sleep(20000); // hack because WaitForSingleObject does not work (matlab spawns as a separate process)
			outputGarment.LoadPanels("arap_l2\\output");
		}

		// Run arcsim to produce simulated result
		outputGarment.SetVertsPos(targetGarment.GetVertsPos());
		outputGarment.Save("arcsim-0.2.1-windows\\cloth_out.obj"); 
		sprintf(cmdLine, "/C adaptiveCloth-2.0.exe simulateoffline params2.json output_%.2d", iter);
		RunProcess("arcsim-0.2.1-windows", cmdLine);
		sprintf(buf, "arcsim-0.2.1-windows\\output_%.2d\\0020_00.obj", iter);
		simGarment.Create(buf);
	
		// Pattern correction: compute difference between sim garment and targetGarment and save into outputGarment
		for (unsigned i=0; i<simGarment.GetNumFaces(); i++) {
			auto targetTri3D = targetGarment.GetTriangle3D(i);
			auto simTri3D = simGarment.GetTriangle3D(i);
			auto & outputTri2D = outputGarment.GetTexTriangle(i);

			Matrix3 matTarget3D, matSim3D, matPatterns2D;
			ComputeTrianlgeMatrix(targetTri3D, matTarget3D);
			ComputeTrianlgeMatrix(simTri3D, matSim3D);
			ComputeTrianlgeMatrix(outputTri2D, matPatterns2D);

			Matrix3 mat = matTarget3D * matSim3D.inverse();
			RScalar det = mat.determinant();
			Matrix3 Q = (matTarget3D * matSim3D.inverse()) * matPatterns2D;
			Vector3 v1(Q.col(0));
			Vector3 v2(Q.col(1));

			Quaternion rot;
			ComputeQuaternion(v1.normalized(), v2.normalized(), rot);
			Vector3 vOut1 = outputTri2D.v[1] - outputTri2D.v[0];
			Vector3 vOut2 = rot*vOut1;
			vOut1 = v1.norm()*vOut1.normalized();
			vOut2 = v2.norm()*vOut2.normalized();
			// outputTri2D.v[0] = outputTri2D.v[0];
			outputTri2D.v[1] = outputTri2D.v[0] + vOut1;
			outputTri2D.v[2] = outputTri2D.v[0] + vOut2;
			RScalar area = outputTri2D.Area();
			int a=0;
		}
		// Set the output garment to have the simulated 3d vertex positions
		outputGarment.SetVertsPos(simGarment.GetVertsPos());

		// Stitch triangles
		outputGarment.SavePanels("arap_l2\\input");
		sprintf(cmdLine, "/C start /b matlab -nosplash -nodesktop -minimize -r RunAll -logfile matlab_log.txt");
		RunProcess("arap_l2", cmdLine);
		Sleep(20000); // hack because WaitForSingleObject does not work (matlab spawns as a separate process)
		outputGarment.LoadPanels("arap_l2\\output");
		sprintf(buf, "output\\%s_%.2d.obj", meshName, iter);
		outputGarment.Save(buf);
	}


	return 0;
}